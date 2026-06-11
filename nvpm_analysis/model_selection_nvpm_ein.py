"""Model selection for predicting relative nvPM EIn from hydrogen content and thrust.

Goal
----
Fit candidate baseline-anchored functions g(H, F) where:
  - g(H, F) = relative nvPM EIn versus the 13.8% H baseline
  - H = fuel hydrogen content (%)
  - F = relative thrust = Thrust/100

Experimental measurements are fuel/reference ratios, so each model prediction is:
  y_hat = g(H_fuel, F) / g(H_ref, F)

This keeps the 13.8% hydrogen baseline explicit even when the study reference fuel is not 13.8%.

This script:
  1) Loads the Excel sheet
  2) Fits a variety of models via least squares (or linear regression in transformed space)
  3) Compares via K-fold CV RMSE on log-scale + R^2 on original scale
  4) Reports best model(s) and saves a summary CSV

Run
---
python3 nvpm_analysis/model_selection_nvpm_ein.py \
  --excel "../MIT Dropbox/Tara Housen/PM_emisisons_vs_fuel_properties.xlsx" \
  --sheet "PM Emissions" \
  --outdir nvpm_analysis_outputs
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import KFold


@dataclass
class ModelSpec:
    name: str
    param_names: list[str]

    H_BASELINE: float = 13.8

    def predict(self, p: np.ndarray, H: np.ndarray, F: np.ndarray) -> np.ndarray:  # pragma: no cover
        """Relative EI versus the 13.8% hydrogen baseline: g(H, F)."""
        raise NotImplementedError

    def predict_ratio(self, p: np.ndarray, H_fuel: np.ndarray, H_ref: np.ndarray, F: np.ndarray) -> np.ndarray:
        """Experimental observable: g(H_fuel, F) / g(H_ref, F)."""
        return self.predict(p, H_fuel, F) / self.predict(p, H_ref, F)

    def initial(self, H: np.ndarray, F: np.ndarray, y: np.ndarray) -> np.ndarray:
        return np.zeros(len(self.param_names), dtype=float)


# -------------------- candidate models --------------------

class Poly2(ModelSpec):
    """y = c0 + c1 ΔH + c2 F + c3 ΔH^2 + c4 F^2 + c5 ΔH F"""

    def __init__(self):
        super().__init__("poly2", ["c0", "c1", "c2", "c3", "c4", "c5"])

    def predict(self, p, H, F):
        c0, c1, c2, c3, c4, c5 = p
        return c0 + c1 * H + c2 * F + c3 * H**2 + c4 * F**2 + c5 * H * F


class Poly3(ModelSpec):
    """y = polynomial up to degree 3 in ΔH,F with cross terms"""

    def __init__(self):
        # terms: 1, H, F, H^2, HF, F^2, H^3, H^2F, HF^2, F^3
        super().__init__(
            "poly3",
            ["c0", "cH", "cF", "cH2", "cHF", "cF2", "cH3", "cH2F", "cHF2", "cF3"],
        )

    def predict(self, p, H, F):
        (c0, cH, cF, cH2, cHF, cF2, cH3, cH2F, cHF2, cF3) = p
        return (
            c0
            + cH * H
            + cF * F
            + cH2 * H**2
            + cHF * H * F
            + cF2 * F**2
            + cH3 * H**3
            + cH2F * (H**2) * F
            + cHF2 * H * (F**2)
            + cF3 * F**3
        )


class LogPoly2(ModelSpec):
    """Baseline-anchored log polynomial for g(H,F).

    log(g) = c1*x + c2*x^2 + c3*x*F + c4*x^2*F + c5*x*F^2, x = H - 13.8.
    This enforces g(13.8, F)=1 for every thrust.
    """

    def __init__(self):
        super().__init__("log-poly2", ["c1", "c2", "c3", "c4", "c5"])

    def predict(self, p, H, F):
        c1, c2, c3, c4, c5 = p
        x = H - self.H_BASELINE
        logy = c1 * x + c2 * x**2 + c3 * x * F + c4 * x**2 * F + c5 * x * F**2
        return np.exp(np.clip(logy, -50, 50))


class ICAOExp(ModelSpec):
    """g(H,F) = exp((alpha*F + beta) * (H - 13.8))."""

    def __init__(self):
        super().__init__("icao-family-exp", ["alpha", "beta"])

    def predict(self, p, H, F):
        alpha, beta = p
        x = H - self.H_BASELINE
        return np.exp(np.clip((alpha * F + beta) * x, -50, 50))

    def initial(self, H, F, y):
        # start near ICAO
        return np.array([0.99, -1.05], dtype=float)


class MechanisticICAORatio(ModelSpec):
    """g(H,F) = exp((a*F^2 + b*F + c) * (H - 13.8))."""

    def __init__(self):
        super().__init__("mechanistic-icao-ratio", ["a_F2", "b_F", "c"])

    def predict(self, p, H, F):
        a, b, c = p
        x = H - self.H_BASELINE
        return np.exp(np.clip((a * F**2 + b * F + c) * x, -50, 50))

    def initial(self, H, F, y):
        return np.array([0.0, 0.99, -1.05], dtype=float)


class PowerLawExp(ModelSpec):
    """g(H,F) = exp((a*F + b) * signed_power(H - 13.8, p))."""

    def __init__(self):
        super().__init__("power-law-exp", ["a", "b", "p_raw"])

    @staticmethod
    def _p(p_raw: float) -> float:
        return 0.15 + 2.85 / (1.0 + np.exp(-p_raw))

    def predict(self, p, H, F):
        a, b, p_raw = p
        power = self._p(p_raw)
        x = H - self.H_BASELINE
        H_power = np.sign(x) * (np.abs(x) ** power)
        return np.exp(np.clip((a * F + b) * H_power, -50, 50))

    def initial(self, H, F, y):
        return np.array([0.99, -1.05, 0.0], dtype=float)


class SaturatingExp(ModelSpec):
    """g(H,F) = exp(-A(F) * (1 - exp(-k*(H - 13.8))))."""

    def __init__(self):
        super().__init__("saturating-exp", ["a", "b", "k_raw"])

    @staticmethod
    def _softplus(x):
        return np.logaddexp(0.0, x)

    def predict(self, p, H, F):
        a, b, k_raw = p
        A = self._softplus(a + b * F)
        k = self._softplus(k_raw)
        x = H - self.H_BASELINE
        logy = -A * (1.0 - np.exp(np.clip(-k * x, -50, 50)))
        return np.exp(np.clip(logy, -50, 50))

    def initial(self, H, F, y):
        return np.array([0.0, 0.0, 0.0], dtype=float)


class QuadRational(ModelSpec):
    """Quadratic/rational baseline model.

    g(H,F) = (1 - Hhat) * ((a + bF)Hhat + 1), Hhat=(H-13.8)/(H_inf-13.8).
    Experimental ratios are g(H_fuel,F)/g(H_ref,F).
    """

    def __init__(self):
        super().__init__("quad-rational", ["a", "b", "H_inf"])

    def predict(self, p, H, F):
        a, b, H_inf = p
        Hhat = (H - self.H_BASELINE) / (H_inf - self.H_BASELINE)
        return (1 - Hhat) * (((a + b * F) * Hhat) + 1)

    def initial(self, H, F, y):
        upper = max(16.0, float(np.nanmax(H)) + 0.5)
        return np.array([-1.1, 1.4, upper], dtype=float)


# -------------------- fitting helpers --------------------

from scipy.optimize import least_squares
from sklearn.metrics import r2_score


def fit_least_squares(
    spec: ModelSpec,
    H: np.ndarray,
    F: np.ndarray,
    y: np.ndarray,
    bounds: tuple[np.ndarray, np.ndarray] | None = None,
) -> np.ndarray:
    """Fit direct baseline-relative values g(H,F)."""
    p0 = spec.initial(H, F, y)

    def fun(p):
        yhat = spec.predict(p, H, F)
        if np.any(~np.isfinite(yhat)):
            return np.full_like(y, 1e6)
        return yhat - y

    if bounds is None:
        res = least_squares(fun, p0, max_nfev=20000)
    else:
        lb, ub = bounds
        res = least_squares(fun, p0, bounds=(lb, ub), max_nfev=20000)

    return res.x


def fit_least_squares_ratio(
    spec: ModelSpec,
    H_fuel: np.ndarray,
    H_ref: np.ndarray,
    F: np.ndarray,
    y: np.ndarray,
    bounds: tuple[np.ndarray, np.ndarray] | None = None,
) -> np.ndarray:
    """Fit observed fuel/reference ratios: g(H_fuel,F)/g(H_ref,F)."""
    p0 = spec.initial(H_fuel, F, y)

    def fun(p):
        yhat = spec.predict_ratio(p, H_fuel, H_ref, F)
        if np.any(~np.isfinite(yhat)):
            return np.full_like(y, 1e6)
        return yhat - y

    if bounds is None:
        res = least_squares(fun, p0, max_nfev=20000)
    else:
        lb, ub = bounds
        res = least_squares(fun, p0, bounds=(lb, ub), max_nfev=20000)

    return res.x


def quad_rational_is_monotone_decreasing(
    p: np.ndarray,
    H_range: tuple[float, float],
    F_grid: np.ndarray | None = None,
    nH: int = 200,
) -> bool:
    """Check monotone decreasing in absolute H for the baseline quad-rational model across an F grid."""

    a, b, H_inf = p
    if not np.isfinite(H_inf) or H_inf <= max(ModelSpec.H_BASELINE + 1e-6, H_range[1] + 1e-6):
        return False

    if F_grid is None:
        F_grid = np.linspace(0.05, 1.0, 10)

    H = np.linspace(H_range[0], H_range[1], nH)
    for F in F_grid:
        yhat = QuadRational().predict(np.array([a, b, H_inf]), H, np.full_like(H, F))
        if np.any(np.diff(yhat) > 1e-8):
            return False
    return True


def fit_quad_rational_constrained(
    H: np.ndarray,
    F: np.ndarray,
    y: np.ndarray,
    H_range: tuple[float, float],
    n_restarts: int = 40,
    seed: int = 0,
    H_ref: np.ndarray | None = None,
) -> np.ndarray:
    """Fit baseline quad-rational with constraints:

    - H_inf is beyond the observed H range and above 13.8 (handled as bound)
    - monotone decreasing in H over the observed H_range for a grid of F

    Strategy: random-restart bounded least squares + accept first/best feasible solution.
    """

    rng = np.random.default_rng(seed)
    spec = QuadRational()

    # Bounds: a and b fairly wide; H_inf constrained beyond observed H and above 13.8.
    H_inf_min = max(ModelSpec.H_BASELINE + 1e-6, H_range[1] + 1e-6)
    lb = np.array([-20.0, -20.0, H_inf_min])
    ub = np.array([20.0, 20.0, max(30.0, H_inf_min + 10.0)])

    best_p = None
    best_sse = np.inf
    best_any_p = None
    best_any_sse = np.inf

    # include the default initial guess as first attempt
    p0_default = np.clip(spec.initial(H, F, y), lb + 1e-9, ub - 1e-9)
    initials = [p0_default]

    # also try the unconstrained solution; often already feasible
    try:
        if H_ref is None:
            p_unconstrained = fit_least_squares(spec, H, F, y)
        else:
            p_unconstrained = fit_least_squares_ratio(spec, H, H_ref, F, y)
        p_unconstrained = np.clip(p_unconstrained, lb + 1e-9, ub - 1e-9)
        initials.append(p_unconstrained)
    except Exception:
        pass
    for _ in range(n_restarts - 1):
        a0 = rng.uniform(-5, 1)
        b0 = rng.uniform(-1, 5)
        H_inf0 = rng.uniform(H_inf_min, max(16.0, H_range[1] + 2.0))
        initials.append(np.array([a0, b0, H_inf0], dtype=float))

    for p0 in initials:
        def fun(p):
            if H_ref is None:
                yhat = spec.predict(p, H, F)
            else:
                yhat = spec.predict_ratio(p, H, H_ref, F)
            if np.any(~np.isfinite(yhat)):
                return np.full_like(y, 1e6)
            return yhat - y

        res = least_squares(fun, p0, bounds=(lb, ub), max_nfev=20000)
        p = res.x

        if H_ref is None:
            yhat_p = spec.predict(p, H, F)
        else:
            yhat_p = spec.predict_ratio(p, H, H_ref, F)
        sse = float(np.sum((yhat_p - y) ** 2))
        if sse < best_any_sse:
            best_any_sse = sse
            best_any_p = p

        if not quad_rational_is_monotone_decreasing(p, H_range=H_range):
            continue

        if sse < best_sse:
            best_sse = sse
            best_p = p

    if best_p is None:
        if best_any_p is not None:
            return best_any_p
        raise RuntimeError(
            "Could not fit baseline quad-rational model. Try increasing restarts or using a different model family."
        )

    return best_p


def rmse(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.sqrt(np.mean((a - b) ** 2)))


def safe_log(y: np.ndarray) -> np.ndarray:
    # avoid log(0)
    eps = np.nanmin(y[y > 0]) * 0.5 if np.any(y > 0) else 1e-6
    return np.log(np.clip(y, eps, None))


@dataclass
class Score:
    name: str
    n_params: int
    cv_rmse_log: float
    cv_rmse: float
    cv_r2: float
    params_full: np.ndarray


def score_model(
    spec: ModelSpec,
    H: np.ndarray,
    F: np.ndarray,
    y: np.ndarray,
    k: int = 5,
    seed: int = 0,
    constrained_quad_rational: bool = False,
    H_range: tuple[float, float] | None = None,
    H_ref: np.ndarray | None = None,
) -> Score:
    kf = KFold(n_splits=k, shuffle=True, random_state=seed)

    rmses_log = []
    rmses = []
    r2s = []

    if constrained_quad_rational and H_range is None:
        H_range = (float(np.min(H)), float(np.max(H)))

    for tr, te in kf.split(H):
        H_ref_tr = None if H_ref is None else H_ref[tr]
        H_ref_te = None if H_ref is None else H_ref[te]
        if constrained_quad_rational and isinstance(spec, QuadRational):
            p = fit_quad_rational_constrained(H[tr], F[tr], y[tr], H_range=H_range, seed=seed, H_ref=H_ref_tr)
        elif H_ref is not None:
            p = fit_least_squares_ratio(spec, H[tr], H_ref_tr, F[tr], y[tr])
        else:
            p = fit_least_squares(spec, H[tr], F[tr], y[tr])

        if H_ref is not None:
            yhat = spec.predict_ratio(p, H[te], H_ref_te, F[te])
        else:
            yhat = spec.predict(p, H[te], F[te])

        rmses.append(rmse(y[te], yhat))
        rmses_log.append(rmse(safe_log(y[te]), safe_log(yhat)))
        r2s.append(r2_score(y[te], yhat))

    if constrained_quad_rational and isinstance(spec, QuadRational):
        p_full = fit_quad_rational_constrained(H, F, y, H_range=H_range, seed=seed, H_ref=H_ref)
    elif H_ref is not None:
        p_full = fit_least_squares_ratio(spec, H, H_ref, F, y)
    else:
        p_full = fit_least_squares(spec, H, F, y)

    return Score(
        name=spec.name,
        n_params=len(spec.param_names),
        cv_rmse_log=float(np.mean(rmses_log)),
        cv_rmse=float(np.mean(rmses)),
        cv_r2=float(np.mean(r2s)),
        params_full=p_full,
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--excel", required=True)
    ap.add_argument("--sheet", default="PM Emissions")
    ap.add_argument("--outdir", default="nvpm_analysis_outputs")
    ap.add_argument("--kfold", type=int, default=5)
    args = ap.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    df = pd.read_excel(Path(args.excel).expanduser(), sheet_name=args.sheet)

    # required cols
    req = ["relative nvPM EIn", "Hydrogen", "Ref Hydrogen", "Thrust"]
    missing = [c for c in req if c not in df.columns]
    if missing:
        raise SystemExit(f"Missing required columns: {missing}")

    df = df.copy()
    df["F"] = df["Thrust"] / 100.0

    mask = np.isfinite(df["relative nvPM EIn"]) & np.isfinite(df["Hydrogen"]) & np.isfinite(df["Ref Hydrogen"]) & np.isfinite(df["F"])
    d = df.loc[mask].copy()

    y = d["relative nvPM EIn"].to_numpy(float)
    H = d["Hydrogen"].to_numpy(float)
    H_ref = d["Ref Hydrogen"].to_numpy(float)
    F = d["F"].to_numpy(float)

    # keep only positive y for models that use exp/log (we still score on same set)
    pos = y > 0
    if np.mean(pos) < 0.98:
        # drop only the zero/neg points (rare)
        y, H, H_ref, F = y[pos], H[pos], H_ref[pos], F[pos]

    specs: list[ModelSpec] = [
        ICAOExp(),
        MechanisticICAORatio(),
        PowerLawExp(),
        SaturatingExp(),
        QuadRational(),
        Poly2(),
        Poly3(),
        LogPoly2(),
    ]

    H_range = (float(np.min(H)), float(np.max(H)))

    scores: list[Score] = []
    for s in specs:
        sc = score_model(
            s,
            H,
            F,
            y,
            k=args.kfold,
            constrained_quad_rational=True,
            H_range=H_range,
            H_ref=H_ref,
        )
        scores.append(sc)

    # table
    rows = []
    for sc in scores:
        rows.append(
            {
                "model": sc.name,
                "n_params": sc.n_params,
                "cv_rmse_log": sc.cv_rmse_log,
                "cv_rmse": sc.cv_rmse,
                "cv_r2": sc.cv_r2,
                "params_full": ",".join([f"{v:.6g}" for v in sc.params_full]),
            }
        )

    out = pd.DataFrame(rows).sort_values(["cv_rmse_log", "cv_rmse"]).reset_index(drop=True)
    out.to_csv(outdir / "ein_model_selection_summary.csv", index=False)

    print("\nEIn model selection using baseline g(H,F) relative to 13.8%; predictions are g(H_fuel,F)/g(H_ref,F) (sorted by CV RMSE on log-scale):")
    print(out[["model", "n_params", "cv_rmse_log", "cv_rmse", "cv_r2"]].to_string(index=False))


if __name__ == "__main__":
    main()
