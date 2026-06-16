"""Diagnostics plots for multiple EIn models (parity, residuals, bootstrap parity band).

Models included:
  - ICAO-family exponential (fit alpha,beta)
  - Quad-rational (unconstrained)
  - Quad-rational (constrained: H_inf>13.8 + monotone decreasing in H)
  - log-poly2 (log(y) quadratic in H,F)

Outputs (in outdir):
  - ein_parity_<model>.png
  - ein_residuals_<model>.png
  - ein_parity_bootstrap_<model>.png  (for constrained quad-rational)

Run:
python3 nvpm_analysis/ein_model_diagnostics.py \
  --excel nvpm_analysis/PM_emisisons_vs_fuel_properties.xlsx \
  --sheet "PM Emissions" \
  --outdir nvpm_analysis_outputs \
  --nboot 1000
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import least_squares
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import GroupKFold, KFold

from model_selection_nvpm_ein import (
    ICAOExp,
    LogPoly2,
    MechanisticICAORatio,
    PowerLawExp,
    QuadRational,
    SaturatingExp,
    fit_least_squares,
    fit_least_squares_ratio,
    fit_quad_rational_constrained,
)


def rmse(y, yhat):
    return float(np.sqrt(np.mean((y - yhat) ** 2)))


def safe_log(y: np.ndarray) -> np.ndarray:
    eps = np.nanmin(y[y > 0]) * 0.5 if np.any(y > 0) else 1e-6
    return np.log(np.clip(y, eps, None))


def cv_metrics(y: np.ndarray, yhat: np.ndarray) -> dict[str, float]:
    finite = np.isfinite(y) & np.isfinite(yhat) & (y > 0) & (yhat > 0)
    if np.sum(finite) < 2:
        return {"rmse_log": np.nan, "rmse": np.nan, "r2": np.nan}
    return {
        "rmse_log": rmse(safe_log(y[finite]), safe_log(yhat[finite])),
        "rmse": rmse(y[finite], yhat[finite]),
        "r2": float(r2_score(y[finite], yhat[finite])),
    }


def bootstrap_residual_band(y: np.ndarray, yhat: np.ndarray, resid: np.ndarray, nboot: int, seed: int = 42):
    rng = np.random.default_rng(seed)
    boot = np.zeros((nboot, len(yhat)))
    for i in range(nboot):
        e = rng.choice(resid, size=len(resid), replace=True)
        boot[i, :] = np.clip(yhat + e, 0, None)
    lo = np.percentile(boot, 2.5, axis=0)
    hi = np.percentile(boot, 97.5, axis=0)
    return lo, hi


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--excel", required=True)
    ap.add_argument("--sheet", default="PM Emissions")
    ap.add_argument("--outdir", default="nvpm_analysis_outputs")
    ap.add_argument("--nboot", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--cv-folds", type=int, default=5, help="Number of folds for row-wise and grouped CV diagnostics.")
    ap.add_argument("--cv-repeats", type=int, default=20, help="Number of repeated row-wise K-fold CV splits.")
    args = ap.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    df = pd.read_excel(Path(args.excel).expanduser(), sheet_name=args.sheet)
    req = ["relative nvPM EIn", "Hydrogen", "Ref Hydrogen", "Thrust"]
    missing = [c for c in req if c not in df.columns]
    if missing:
        raise SystemExit(f"Missing required columns: {missing}")

    df = df.copy()
    df["F"] = df["Thrust"] / 100.0

    mask = (
        np.isfinite(df["relative nvPM EIn"])
        & np.isfinite(df["Hydrogen"])
        & np.isfinite(df["Ref Hydrogen"])
        & np.isfinite(df["F"])
        & (df["relative nvPM EIn"] > 0)
    )
    d = df.loc[mask].copy()

    y = d["relative nvPM EIn"].to_numpy(float)
    H = d["Hydrogen"].to_numpy(float)
    H_abs = H
    H_ref = d["Ref Hydrogen"].to_numpy(float)
    F = d["F"].to_numpy(float)

    H_range = (float(np.min(H)), float(np.max(H)))

    models = []
    display_names = {
        "icao_family_exp": "ICAO-Family Exponential",
        "mechanistic_icao_ratio": "Mechanistic ICAO Ratio",
        "power_law_exp": "Power-Law Exponential",
        "saturating_exp": "Saturating Exponential",
        "log_poly2": "Log-Polynomial (2nd Order)",
        "quad_rational": "Quadratic Rational",
        "quad_rational_constrained": "Quadratic Rational Constrained",
    }
    param_names = {
        "icao_family_exp": spec_icao.param_names if "spec_icao" in locals() else ["alpha", "beta"],
        "mechanistic_icao_ratio": ["a_F2", "b_F", "c"],
        "power_law_exp": ["a", "b", "p_raw"],
        "saturating_exp": ["a", "b", "k_raw"],
        "log_poly2": ["c1", "c2", "c3", "c4", "c5"],
        "quad_rational": ["a", "b", "H_inf"],
        "quad_rational_constrained": ["a", "b", "H_inf"],
    }

    # ICAO-family exponential (fit alpha,beta)
    spec_icao = ICAOExp()
    param_names["icao_family_exp"] = spec_icao.param_names
    p_icao = fit_least_squares_ratio(spec_icao, H, H_ref, F, y)
    yhat_icao = spec_icao.predict_ratio(p_icao, H, H_ref, F)
    models.append(("icao_family_exp", p_icao, yhat_icao))

    # mechanistic ICAO ratio with nonlinear thrust coefficient
    spec_micao = MechanisticICAORatio()
    p_micao = fit_least_squares_ratio(spec_micao, H, H_ref, F, y)
    yhat_micao = spec_micao.predict_ratio(p_micao, H, H_ref, F)
    models.append(("mechanistic_icao_ratio", p_micao, yhat_micao))

    # power-law exponential
    spec_power = PowerLawExp()
    p_power = fit_least_squares_ratio(spec_power, H, H_ref, F, y)
    yhat_power = spec_power.predict_ratio(p_power, H, H_ref, F)
    models.append(("power_law_exp", p_power, yhat_power))

    # saturating exponential
    spec_sat = SaturatingExp()
    p_sat = fit_least_squares_ratio(spec_sat, H, H_ref, F, y)
    yhat_sat = spec_sat.predict_ratio(p_sat, H, H_ref, F)
    models.append(("saturating_exp", p_sat, yhat_sat))

    # log-poly2
    spec_lp2 = LogPoly2()
    p_lp2 = fit_least_squares_ratio(spec_lp2, H, H_ref, F, y)
    yhat_lp2 = spec_lp2.predict_ratio(p_lp2, H, H_ref, F)
    models.append(("log_poly2", p_lp2, yhat_lp2))

    # quad-rational unconstrained
    spec_qr = QuadRational()
    p_qr = fit_least_squares_ratio(spec_qr, H, H_ref, F, y)
    yhat_qr = spec_qr.predict_ratio(p_qr, H, H_ref, F)
    models.append(("quad_rational", p_qr, yhat_qr))

    # quad-rational constrained
    p_qrc = fit_quad_rational_constrained(H, F, y, H_range=H_range, seed=args.seed, H_ref=H_ref)
    yhat_qrc = spec_qr.predict_ratio(p_qrc, H, H_ref, F)
    models.append(("quad_rational_constrained", p_qrc, yhat_qrc))

    specs_by_name = {
        "icao_family_exp": spec_icao,
        "mechanistic_icao_ratio": spec_micao,
        "power_law_exp": spec_power,
        "saturating_exp": spec_sat,
        "log_poly2": spec_lp2,
        "quad_rational": spec_qr,
        "quad_rational_constrained": spec_qr,
    }
    model_categories = {
        "icao_family_exp": "physical_candidate",
        "mechanistic_icao_ratio": "physical_candidate",
        "power_law_exp": "physical_candidate",
        "saturating_exp": "physical_candidate",
        "quad_rational": "physical_candidate",
        "quad_rational_constrained": "physical_candidate",
        "log_poly2": "semi_flexible_empirical_benchmark",
    }

    def _predict_model(name: str, p: np.ndarray, Hv: np.ndarray, Fv: np.ndarray) -> np.ndarray:
        return specs_by_name[name].predict(p, Hv, Fv)

    # marker mapping (copied from your original script)
    def build_marker_dict(pairs: np.ndarray) -> dict[str, str]:
        markers = [
            "o",
            "s",
            "3",
            "D",
            "+",
            "^",
            "v",
            "P",
            "*",
            "8",
            "X",
            "<",
            ">",
            "h",
            "H",
            "x",
            "d",
            "p",
            "4",
        ]
        pair_list = np.unique(pairs)
        return {str(pair).strip(): markers[i % len(markers)] for i, pair in enumerate(pair_list)}

    # pair key
    engine = d["Engine"].astype(str) if "Engine" in d.columns else pd.Series(["" for _ in range(len(d))])
    campaign = d["Campaign"].astype(str) if "Campaign" in d.columns else pd.Series(["" for _ in range(len(d))])
    pairs = (engine + " / " + campaign).to_numpy()
    pair_list = np.unique(pairs)
    marker_dict = build_marker_dict(pairs)

    def _fit_predict_for_cv(name: str, tr: np.ndarray, te: np.ndarray) -> np.ndarray:
        spec = specs_by_name[name]
        if name == "quad_rational_constrained":
            p_cv = fit_quad_rational_constrained(
                H[tr],
                F[tr],
                y[tr],
                H_range=H_range,
                seed=args.seed,
                H_ref=H_ref[tr],
                n_restarts=20,
            )
        else:
            p_cv = fit_least_squares_ratio(spec, H[tr], H_ref[tr], F[tr], y[tr])
        return spec.predict_ratio(p_cv, H[te], H_ref[te], F[te])

    def _summarize_cv_rows(rows: list[dict[str, float | str | int]]) -> pd.DataFrame:
        cv = pd.DataFrame(rows)
        metric_cols = ["rmse_log", "rmse", "r2"]
        grouped = (
            cv.groupby(["validation", "model", "display_name", "category"], dropna=False)[metric_cols]
            .agg(["mean", "std", "min", "max", "count"])
            .reset_index()
        )
        grouped.columns = ["_".join([str(x) for x in col if str(x)]) for col in grouped.columns.to_flat_index()]
        return grouped.sort_values(["validation", "category", "rmse_log_mean", "rmse_mean"]).reset_index(drop=True)

    cv_rows: list[dict[str, float | str | int]] = []
    cv_model_names = list(specs_by_name)
    for repeat in range(args.cv_repeats):
        kf = KFold(n_splits=args.cv_folds, shuffle=True, random_state=args.seed + repeat)
        for fold, (tr, te) in enumerate(kf.split(H)):
            for name in cv_model_names:
                try:
                    yhat_cv = _fit_predict_for_cv(name, tr, te)
                    metrics = cv_metrics(y[te], yhat_cv)
                except Exception:
                    metrics = {"rmse_log": np.nan, "rmse": np.nan, "r2": np.nan}
                cv_rows.append(
                    {
                        "validation": "rowwise_repeated_kfold",
                        "repeat": repeat,
                        "fold": fold,
                        "model": name,
                        "display_name": display_names[name],
                        "category": model_categories.get(name, "uncategorized"),
                        **metrics,
                    }
                )

    for group_col in ["Campaign", "Source"]:
        if group_col not in d.columns:
            continue
        groups = d[group_col].astype(str).fillna("missing").to_numpy()
        n_groups = len(np.unique(groups))
        if n_groups < 2:
            continue
        gkf = GroupKFold(n_splits=min(args.cv_folds, n_groups))
        for fold, (tr, te) in enumerate(gkf.split(H, y, groups=groups)):
            held_out = ";".join(sorted(np.unique(groups[te])))
            for name in cv_model_names:
                try:
                    yhat_cv = _fit_predict_for_cv(name, tr, te)
                    metrics = cv_metrics(y[te], yhat_cv)
                except Exception:
                    metrics = {"rmse_log": np.nan, "rmse": np.nan, "r2": np.nan}
                cv_rows.append(
                    {
                        "validation": f"grouped_kfold_by_{group_col.lower()}",
                        "repeat": 0,
                        "fold": fold,
                        "held_out_groups": held_out,
                        "model": name,
                        "display_name": display_names[name],
                        "category": model_categories.get(name, "uncategorized"),
                        **metrics,
                    }
                )

    cv_detail = pd.DataFrame(cv_rows)
    cv_summary = _summarize_cv_rows(cv_rows)
    cv_detail.to_csv(outdir / "ein_cv_diagnostics_detail.csv", index=False)
    cv_summary.to_csv(outdir / "ein_cv_diagnostics_summary.csv", index=False)

    import matplotlib.pyplot as plt

    cmap = plt.get_cmap("tab20")
    color_dict = {pair: cmap(i % cmap.N) for i, pair in enumerate(pair_list)}

    summary_rows = []

    for name, p, yhat in models:
        resid = y - yhat
        r2 = r2_score(y, yhat)
        e = rmse(y, yhat)
        mae = float(mean_absolute_error(y, yhat))
        params = {nm: float(val) for nm, val in zip(param_names[name], p)}
        summary_rows.append(
            {
                "model": name,
                "display_name": display_names[name],
                "r2": r2,
                "rmse": e,
                "mae": mae,
                "n": len(y),
                **params,
            }
        )

        vmin = float(np.min(np.r_[y, yhat]))
        vmax = float(np.max(np.r_[y, yhat]))

        # parity plot (marker per engine/campaign)
        plt.figure(figsize=(7.2, 5.6))
        for pair in pair_list:
            m = pairs == pair
            if not np.any(m):
                continue
            plt.scatter(
                y[m],
                yhat[m],
                s=65,
                alpha=0.8,
                marker=marker_dict[str(pair)],
                color=color_dict[pair],
                edgecolor="k",
                linewidth=0.4,
                label=pair,
            )

        plt.plot([vmin, vmax], [vmin, vmax], "k--", lw=2)
        plt.gca().set_aspect("equal", adjustable="box")
        plt.xlim(vmin, vmax)
        plt.ylim(vmin, vmax)
        plt.grid(True, ls="--", alpha=0.3)
        plt.xlabel("Experimental relative nvPM EIn")
        plt.ylabel("Model relative nvPM EIn")
        plt.title(f"Parity plot: {display_names[name]}\n$R^2$={r2:.3f}, RMSE={e:.3f}, n={len(y)}")
        plt.legend(bbox_to_anchor=(1.03, 1), loc="upper left", fontsize=8, title="Engine / Campaign")
        plt.tight_layout()
        plt.savefig(outdir / f"ein_parity_{name}.png", dpi=220, bbox_inches="tight")
        plt.close()

        # residual plot
        plt.figure(figsize=(7.2, 5.2))
        for pair in pair_list:
            m = pairs == pair
            if not np.any(m):
                continue
            plt.scatter(
                yhat[m],
                resid[m],
                s=65,
                alpha=0.8,
                marker=marker_dict[str(pair)],
                color=color_dict[pair],
                edgecolor="k",
                linewidth=0.4,
                label=pair,
            )

        plt.axhline(0, color="k", ls="--", lw=2)
        plt.grid(True, ls="--", alpha=0.3)
        plt.xlabel("Model relative nvPM EIn")
        plt.ylabel("Residual (Exp - Model)")
        plt.title(f"Residuals: {display_names[name]}")
        plt.legend(bbox_to_anchor=(1.03, 1), loc="upper left", fontsize=8, title="Engine / Campaign")
        plt.tight_layout()
        plt.savefig(outdir / f"ein_residuals_{name}.png", dpi=220, bbox_inches="tight")
        plt.close()

        # bootstrap parity band (only for constrained quad-rational)
        if name == "quad_rational_constrained":
            lo, hi = bootstrap_residual_band(y, yhat, resid, nboot=args.nboot, seed=args.seed)
            sort = np.argsort(yhat)

            plt.figure(figsize=(7.2, 5.6))
            plt.fill_between(
                yhat[sort],
                lo[sort],
                hi[sort],
                color="lightgray",
                alpha=0.85,
                label="bootstrap 95% CI (residual)",
                zorder=1,
            )

            for pair in pair_list:
                m = pairs == pair
                if not np.any(m):
                    continue
                plt.scatter(
                    y[m],
                    yhat[m],
                    s=65,
                    alpha=0.8,
                    marker=marker_dict[str(pair)],
                    color=color_dict[pair],
                    edgecolor="k",
                    linewidth=0.4,
                    label=pair,
                    zorder=3,
                )

            plt.plot([vmin, vmax], [vmin, vmax], "k--", lw=2, zorder=4)
            plt.gca().set_aspect("equal", adjustable="box")
            plt.xlim(vmin, vmax)
            plt.ylim(vmin, vmax)
            plt.grid(True, ls="--", alpha=0.3)
            plt.xlabel("Experimental relative nvPM EIn")
            plt.ylabel("Model relative nvPM EIn")
            plt.title(f"Bootstrap parity CI: {display_names[name]}\n$R^2$={r2:.3f}, nboot={args.nboot}")
            plt.legend(bbox_to_anchor=(1.03, 1), loc="upper left", fontsize=8, title="Engine / Campaign")
            plt.tight_layout()
            plt.savefig(outdir / f"ein_parity_bootstrap_{name}.png", dpi=220, bbox_inches="tight")
            plt.close()

    # combined side-by-side parity and residual figures with one shared legend
    def _plot_combined(kind: str) -> None:
        ncols = min(4, len(models))
        nrows = int(np.ceil(len(models) / ncols))
        fig, axes = plt.subplots(nrows, ncols, figsize=(4.6 * ncols, 4.4 * nrows), sharex=False, sharey=False)
        axes = np.atleast_1d(axes).ravel()
        for extra_ax in axes[len(models):]:
            extra_ax.axis("off")

        legend_handles = []
        legend_labels = []
        for ax, (name, _p, yhat) in zip(axes, models):
            resid = y - yhat
            r2 = r2_score(y, yhat)
            e = rmse(y, yhat)
            if kind == "parity":
                xvals = y
                yvals = yhat
                vmin = float(np.min(np.r_[y, yhat]))
                vmax = float(np.max(np.r_[y, yhat]))
                ax.plot([vmin, vmax], [vmin, vmax], "k--", lw=1.5)
                ax.set_xlim(vmin, vmax)
                ax.set_ylim(vmin, vmax)
                ax.set_aspect("equal", adjustable="box")
                ax.set_xlabel("Experimental relative nvPM EIn")
                ax.set_ylabel("Model relative nvPM EIn")
                ax.set_title(f"{display_names[name]}\n$R^2$={r2:.3f}, RMSE={e:.3f}")
            else:
                xvals = yhat
                yvals = resid
                ax.axhline(0, color="k", ls="--", lw=1.5)
                ax.set_xlabel("Model relative nvPM EIn")
                ax.set_ylabel("Residual (Exp - Model)")
                ax.set_title(display_names[name])

            for pair in pair_list:
                m = pairs == pair
                if not np.any(m):
                    continue
                sc = ax.scatter(
                    xvals[m],
                    yvals[m],
                    s=45,
                    alpha=0.8,
                    marker=marker_dict[str(pair)],
                    color=color_dict[pair],
                    edgecolor="k",
                    linewidth=0.35,
                    label=pair,
                )
                if kind == "parity" and name == models[0][0]:
                    legend_handles.append(sc)
                    legend_labels.append(pair)
            ax.grid(True, ls="--", alpha=0.3)

        fig.suptitle(
            "EIn parity plots by model function" if kind == "parity" else "EIn residuals by model function",
            y=1.03,
            fontsize=14,
        )
        fig.legend(
            legend_handles,
            legend_labels,
            bbox_to_anchor=(0.5, -0.03),
            loc="upper center",
            ncol=min(4, max(1, len(legend_labels))),
            fontsize=8,
            title="Engine / Campaign",
        )
        fig.tight_layout()
        fig.savefig(outdir / f"ein_{kind}_all_models.png", dpi=220, bbox_inches="tight")
        plt.close(fig)

    _plot_combined("parity")
    _plot_combined("residuals")

    summary = pd.DataFrame(summary_rows)
    summary.to_csv(outdir / "ein_model_diagnostics_summary.csv", index=False)
    summary.to_html(outdir / "ein_model_diagnostics_summary.html", index=False, float_format=lambda x: f"{x:.4g}")

    # response curves with 95% bootstrap confidence bands for every model; highlight best fit
    best_row = summary.sort_values(["rmse", "mae"], ascending=True).iloc[0]
    best_name = str(best_row["model"])

    rng = np.random.default_rng(args.seed)
    H_grid_abs = np.linspace(float(np.nanmin(H_abs)), float(np.nanmax(H_abs)), 140)
    F_grid = np.array([0.07, 0.30, 0.65, 0.85, 1.00])
    H_grid = H_grid_abs
    colors = plt.cm.viridis(np.linspace(0.05, 0.95, len(F_grid)))

    curve_results = {}
    bootstrap_success = {}
    for name, p_hat, yhat in models:
        spec = specs_by_name.get(name)
        resid = y - yhat
        boot_preds = {float(F0): [] for F0 in F_grid}
        successful_boot = 0
        for _ in range(args.nboot):
            e = rng.choice(resid, size=len(resid), replace=True)
            y_star = np.clip(yhat + e, 1e-12, None)
            try:
                if name == "quad_rational_constrained":
                    p_b = fit_quad_rational_constrained(H, F, y_star, H_range=H_range, seed=int(rng.integers(0, 1_000_000)), H_ref=H_ref)
                else:
                    p_b = fit_least_squares_ratio(spec, H, H_ref, F, y_star)
            except Exception:
                continue
            for F0 in F_grid:
                boot_preds[float(F0)].append(_predict_model(name, p_b, H_grid, np.full_like(H_grid, F0)))
            successful_boot += 1

        bands = {}
        for F0 in F_grid:
            preds = np.asarray(boot_preds[float(F0)])
            if len(preds) >= 5:
                lo = np.percentile(preds, 2.5, axis=0)
                med = np.percentile(preds, 50, axis=0)
                hi = np.percentile(preds, 97.5, axis=0)
            else:
                med = _predict_model(name, p_hat, H_grid, np.full_like(H_grid, F0))
                lo = hi = med
            bands[float(F0)] = {"lo": lo, "med": med, "hi": hi}
        curve_results[name] = bands
        bootstrap_success[name] = successful_boot

    ncols = min(4, len(models))
    nrows = int(np.ceil(len(models) / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(4.25 * ncols, 3.9 * nrows), sharex=True, sharey=True)
    axes = np.atleast_1d(axes).ravel()
    for extra_ax in axes[len(models):]:
        extra_ax.axis("off")
    line_handles = []
    for ax, (name, _p, _yhat) in zip(axes, models):
        is_best = name == best_name
        for color, F0 in zip(colors, F_grid):
            band = curve_results[name][float(F0)]
            ax.fill_between(H_grid_abs, band["lo"], band["hi"], color=color, alpha=0.10 if not is_best else 0.18)
            (line,) = ax.plot(
                H_grid_abs,
                band["med"],
                color=color,
                lw=1.5,
                label=f"F/F00={F0:.2f}",
            )
            if name == models[0][0]:
                line_handles.append(line)
        row = summary.loc[summary["model"] == name].iloc[0]
        title = f"{display_names[name]}\nR²={row['r2']:.3f}, RMSE={row['rmse']:.3f}"
        if is_best:
            title = "★ " + title
        ax.set_title(title, pad=12)
        ax.grid(True, ls="--", alpha=0.3)
        ax.set_xlabel("Hydrogen content (%)")
        ax.set_ylabel("relative nvPM EIn")
        ax.tick_params(axis="both", which="both", labelbottom=True, labelleft=True)

    fig.suptitle(
        f"Relative nvPM EIn vs hydrogen: all model functions with 95% residual-bootstrap bands\n"
        "All curves are relative to the 13.8% hydrogen baseline; best fit selected by lowest RMSE",
        fontsize=13,
        y=0.97,
    )
    fig.subplots_adjust(left=0.06, right=0.97, bottom=0.13, top=0.84, wspace=0.18, hspace=0.56)
    fig.legend(
        line_handles,
        [h.get_label() for h in line_handles],
        loc="lower center",
        bbox_to_anchor=(0.48, 0.015),
        ncol=len(F_grid),
        fontsize=8,
        title="Thrust curve",
    )
    fig.savefig(outdir / "ein_all_models_hydrogen_bootstrap_bands.png", dpi=220, bbox_inches="tight")
    fig.savefig(outdir / "ein_best_fit_hydrogen_bootstrap_bands.png", dpi=220, bbox_inches="tight")
    plt.close(fig)

    # Individual cards for the HTML hover-to-enlarge interaction.
    for name, _p, _yhat in models:
        is_best = name == best_name
        fig_i, ax = plt.subplots(figsize=(6.2, 4.4))
        for color, F0 in zip(colors, F_grid):
            band = curve_results[name][float(F0)]
            ax.fill_between(H_grid_abs, band["lo"], band["hi"], color=color, alpha=0.16 if is_best else 0.11)
            ax.plot(H_grid_abs, band["med"], color=color, lw=1.8, label=f"F/F00={F0:.2f}")
        row = summary.loc[summary["model"] == name].iloc[0]
        title = f"{display_names[name]}\nR²={row['r2']:.3f}, RMSE={row['rmse']:.3f}"
        if is_best:
            title = "★ " + title
        ax.set_title(title, pad=10)
        ax.set_xlabel("Hydrogen content (%)")
        ax.set_ylabel("relative nvPM EIn")
        ax.grid(True, ls="--", alpha=0.3)
        fig_i.tight_layout()
        fig_i.savefig(outdir / f"ein_hydrogen_bootstrap_{name}.png", dpi=220, bbox_inches="tight")
        plt.close(fig_i)

    best_summary = {
        "best_model": best_name,
        "display_name": display_names[best_name],
        "selection_rule": "lowest in-sample RMSE, then lowest MAE",
        "r2": float(best_row["r2"]),
        "rmse": float(best_row["rmse"]),
        "mae": float(best_row["mae"]),
        "n": int(best_row["n"]),
        "bootstrap_requested": int(args.nboot),
        "bootstrap_successful_by_model": {k: int(v) for k, v in bootstrap_success.items()},
        "ci_method": "residual bootstrap: resample residuals, add to fitted predictions, refit each model, take 2.5th/97.5th percentiles of baseline-relative predictions",
        "hydrogen_baseline": 13.8,
        "F_grid": F_grid.tolist(),
    }
    import json

    (outdir / "ein_best_fit_bootstrap_summary.json").write_text(json.dumps(best_summary, indent=2), encoding="utf-8")

    print(f"Wrote diagnostics to: {outdir}")
    print(summary[["display_name", "r2", "rmse", "mae", "n"]].to_string(index=False))
    print("\nCV diagnostics: mean ± SD across folds/repeats. Row-wise CV assesses pooled interpolation; grouped CV is a robustness diagnostic for systematic campaign/source heterogeneity.")
    for validation, block in cv_summary.groupby("validation"):
        print(f"\n{validation}")
        compact = block[["category", "display_name", "rmse_log_mean", "rmse_log_std", "rmse_mean", "rmse_std", "r2_mean", "r2_std"]].copy()
        print(compact.to_string(index=False))


if __name__ == "__main__":
    main()
