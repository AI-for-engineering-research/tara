"""Constrained quad-rational model fit for EIn + bootstrap confidence intervals.

Constraints
-----------
1) H_inf > 13.8
2) Monotone decreasing in H over observed H range for a grid of F values.

Bootstrap
---------
Residual bootstrap (like your approach):
  - Fit constrained model
  - Compute residuals
  - For each bootstrap sample: y* = yhat + resampled_residuals
  - Refit constrained model to (H,F,y*)
  - Collect parameter draws and prediction bands

Run
---
python3 nvpm_analysis/constrained_quad_rational_bootstrap.py \
  --excel "../MIT Dropbox/Tara Housen/PM_emisisons_vs_fuel_properties.xlsx" \
  --sheet "PM Emissions" \
  --outdir nvpm_analysis_outputs \
  --nboot 1000
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from model_selection_nvpm_ein import (
    QuadRational,
    fit_quad_rational_constrained,
    quad_rational_is_monotone_decreasing,
)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--excel", required=True)
    ap.add_argument("--sheet", default="PM Emissions")
    ap.add_argument("--outdir", default="nvpm_analysis_outputs")
    ap.add_argument("--nboot", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    df = pd.read_excel(Path(args.excel).expanduser(), sheet_name=args.sheet)
    req = ["relative nvPM EIn", "Hydrogen", "Thrust"]
    missing = [c for c in req if c not in df.columns]
    if missing:
        raise SystemExit(f"Missing required columns: {missing}")

    df = df.copy()
    df["F"] = df["Thrust"] / 100.0

    mask = np.isfinite(df["relative nvPM EIn"]) & np.isfinite(df["Hydrogen"]) & np.isfinite(df["F"]) & (df["relative nvPM EIn"] > 0)
    d = df.loc[mask].copy()

    y = d["relative nvPM EIn"].to_numpy(float)
    H = d["Hydrogen"].to_numpy(float)
    F = d["F"].to_numpy(float)

    H_range = (float(np.min(H)), float(np.max(H)))

    spec = QuadRational()

    # ----- fit constrained model -----
    p_hat = fit_quad_rational_constrained(H, F, y, H_range=H_range, seed=args.seed)
    assert quad_rational_is_monotone_decreasing(p_hat, H_range=H_range)

    yhat = spec.predict(p_hat, H, F)
    resid = y - yhat

    # R^2 on original scale
    ss_res = float(np.sum((y - yhat) ** 2))
    ss_tot = float(np.sum((y - float(np.mean(y))) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")

    # ----- bootstrap refits -----
    rng = np.random.default_rng(args.seed)

    P = np.zeros((args.nboot, 3))
    ok = 0

    for i in range(args.nboot):
        e = rng.choice(resid, size=len(resid), replace=True)
        y_star = np.clip(yhat + e, 1e-12, None)
        try:
            p_b = fit_quad_rational_constrained(H, F, y_star, H_range=H_range, seed=int(rng.integers(0, 1_000_000)))
        except RuntimeError:
            continue
        P[ok, :] = p_b
        ok += 1

    P = P[:ok]

    if ok < max(50, int(args.nboot * 0.2)):
        raise RuntimeError(f"Too few successful bootstrap refits: {ok}/{args.nboot}.")

    # parameter CIs
    param_names = ["a", "b", "H_inf"]
    ci = {}
    for j, nm in enumerate(param_names):
        ci[nm] = (
            float(np.percentile(P[:, j], 2.5)),
            float(np.percentile(P[:, j], 50)),
            float(np.percentile(P[:, j], 97.5)),
        )

    # prediction bands on a grid
    H_grid = np.linspace(H_range[0], H_range[1], 120)
    F_grid = np.array([0.07, 0.30, 0.85, 1.00])  # ICAO-ish modes

    bands = []
    for F0 in F_grid:
        Y = []
        for p in P:
            Y.append(spec.predict(p, H_grid, np.full_like(H_grid, F0)))
        Y = np.asarray(Y)
        lo = np.percentile(Y, 2.5, axis=0)
        hi = np.percentile(Y, 97.5, axis=0)
        med = np.percentile(Y, 50, axis=0)
        bands.append((F0, lo, med, hi))

    # save summary
    import json

    out = {
        "fit": {"a": float(p_hat[0]), "b": float(p_hat[1]), "H_inf": float(p_hat[2])},
        "r2": float(r2),
        "bootstrap_success": int(ok),
        "bootstrap_requested": int(args.nboot),
        "param_ci_95": {k: {"lo": v[0], "median": v[1], "hi": v[2]} for k, v in ci.items()},
        "H_range": {"min": H_range[0], "max": H_range[1]},
        "F_grid": F_grid.tolist(),
    }
    (outdir / "ein_constrained_quad_rational_bootstrap_summary.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )

    # plot
    import matplotlib.pyplot as plt

    plt.figure(figsize=(7.2, 5.2))
    for F0, lo, med, hi in bands:
        plt.fill_between(H_grid, lo, hi, alpha=0.18)
        plt.plot(H_grid, med, lw=2, label=f"F={F0:.2f}")

    plt.scatter(H, y, s=18, alpha=0.35, color="k", label="data")
    plt.xlabel("Hydrogen (%)")
    plt.ylabel("relative nvPM EIn")
    plt.title(f"Constrained quad-rational fit + bootstrap 95% bands\n$R^2$={r2:.3f} (fit on data)")
    plt.legend(ncol=2)
    plt.tight_layout()
    plt.savefig(outdir / "ein_constrained_quad_rational_bootstrap_bands.png", dpi=220)
    plt.close()

    # print summary
    print("\nConstrained quad-rational fit (EIn):")
    print(f"  a={p_hat[0]:.6g}, b={p_hat[1]:.6g}, H_inf={p_hat[2]:.6g}")
    print(f"  R^2={r2:.4f}")
    print(f"  bootstrap successful: {ok}/{args.nboot}")
    print("  95% bootstrap CIs:")
    for nm in param_names:
        lo, med, hi = ci[nm]
        print(f"    {nm}: [{lo:.6g}, {hi:.6g}] (median {med:.6g})")


if __name__ == "__main__":
    main()
