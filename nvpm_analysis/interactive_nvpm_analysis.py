"""Interactive nvPM emissions explorer + model fitting.

Outputs:
  - nvpm_analysis_outputs/nvpm_interactive.html (Plotly interactive)
  - nvpm_analysis_outputs/*.png parity/residual plots
  - printed fit metrics + bootstrap CIs

Assumptions about Excel columns (case-sensitive):
  - 'relative nvPM EIn'
  - 'relative mBC' (used as EIm)
  - 'Hydrogen'
  - 'Ref Hydrogen'
  - optionally 'Aromatics' and 'Ref Aromatics'
  - 'Thrust' (0-100)
  - 'Campaign', 'Engine', 'Fuel', 'Source' (optional for hover)

Run:
  python nvpm_analysis/interactive_nvpm_analysis.py \
    --excel "../MIT Dropbox/Tara Housen/PM_emisisons_vs_fuel_properties.xlsx" \
    --sheet "PM Emissions"
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import least_squares
from sklearn.metrics import r2_score


# ------------------------- models -------------------------

def icao_h_model(H_fuel: np.ndarray, H_ref: np.ndarray, F: np.ndarray, which: str) -> np.ndarray:
    """ICAO exponential hydrogen correction, expressed as relative(fuel)/relative(ref).

    which: 'EIn' uses (0.99*F - 1.05)
           'EIm' uses (1.08*F - 1.31)
    """

    if which == "EIn":
        alpha = 0.99 * F - 1.05
    elif which == "EIm":
        alpha = 1.08 * F - 1.31
    else:
        raise ValueError("which must be 'EIn' or 'EIm'")

    # k_fuel_n = exp(alpha*(13.8 - H)) ; relative EI = 1/k
    rel_fuel_vs_13p8 = np.exp(-alpha * (13.8 - H_fuel))
    rel_ref_vs_13p8 = np.exp(-alpha * (13.8 - H_ref))
    return rel_fuel_vs_13p8 / rel_ref_vs_13p8


def quad_model(params: np.ndarray, H_fuel: np.ndarray, H_ref: np.ndarray, F: np.ndarray) -> np.ndarray:
    """Your quadratic-inspired hydrogen correction model (relative fuel vs ref)."""

    a, b, H_inf = params

    def _k(H: np.ndarray) -> np.ndarray:
        H_hat = (H - 13.8) / (H_inf - 13.8)
        return 1 / ((1 - H_hat) * ((a + b * F) * H_hat + 1))

    k_fuel = _k(H_fuel)
    k_ref = _k(H_ref)

    rel_fuel = 1 / k_fuel
    rel_ref = 1 / k_ref
    return rel_fuel / rel_ref


def residuals(params: np.ndarray, H_fuel: np.ndarray, H_ref: np.ndarray, F: np.ndarray, y: np.ndarray) -> np.ndarray:
    return quad_model(params, H_fuel, H_ref, F) - y


# ------------------------- fitting + bootstrap -------------------------

@dataclass
class FitResult:
    params: np.ndarray
    r2: float
    yhat: np.ndarray
    residuals: np.ndarray
    ci_lower: np.ndarray | None = None
    ci_upper: np.ndarray | None = None


def fit_quadratic(
    y: np.ndarray,
    H_fuel: np.ndarray,
    H_ref: np.ndarray,
    F: np.ndarray,
    initial: tuple[float, float, float],
    n_boot: int = 1000,
    seed: int = 42,
) -> FitResult:
    res = least_squares(residuals, np.array(initial, dtype=float), args=(H_fuel, H_ref, F, y))
    params = res.x
    yhat = quad_model(params, H_fuel, H_ref, F)
    r2 = r2_score(y, yhat)
    resid = y - yhat

    rng = np.random.default_rng(seed)
    boot = np.zeros((n_boot, len(yhat)))
    for i in range(n_boot):
        e = rng.choice(resid, size=len(resid), replace=True)
        boot[i, :] = np.clip(yhat + e, 0, None)

    ci_lower = np.percentile(boot, 2.5, axis=0)
    ci_upper = np.percentile(boot, 97.5, axis=0)

    return FitResult(params=params, r2=r2, yhat=yhat, residuals=resid, ci_lower=ci_lower, ci_upper=ci_upper)


# ------------------------- interactive viz (plotly) -------------------------

def build_interactive(df: pd.DataFrame, out_html: Path, outdir: Path | None = None) -> None:
    import plotly.express as px
    import plotly.graph_objects as go

    # create deltas if columns exist
    if "Hydrogen" in df.columns and "Ref Hydrogen" in df.columns:
        df = df.copy()
        df["ΔH"] = df["Hydrogen"] - df["Ref Hydrogen"]

    if "Aromatics" in df.columns and "Ref Aromatics" in df.columns:
        df = df.copy()
        df["ΔAromatics"] = df["Aromatics"] - df["Ref Aromatics"]

    df["F/F00"] = df["Thrust"] / 100.0
    df["Engine/Campaign"] = df.get("Engine", "").astype(str) + " / " + df.get("Campaign", "").astype(str)

    hover_cols = [
        c
        for c in [
            "Fuel",
            "Source",
            "Engine",
            "Campaign",
            "Thrust",
            "F/F00",
            "Hydrogen",
            "Ref Hydrogen",
            "ΔH",
            "Aromatics",
            "Ref Aromatics",
            "ΔAromatics",
        ]
        if c in df.columns
    ]

    # ---- (1) requested scatter: change in hydrogen vs relative nvPM EIn, colored by thrust ----
    if "relative nvPM EIn" not in df.columns:
        raise ValueError("Could not find 'relative nvPM EIn' for y-axis.")
    if "ΔH" not in df.columns:
        raise ValueError("Could not compute 'ΔH' = Hydrogen - Ref Hydrogen for x-axis.")

    scatter_df = df[np.isfinite(df["relative nvPM EIn"]) & np.isfinite(df["ΔH"]) & np.isfinite(df["F/F00"])].copy()
    fig_scatter = px.scatter(
        scatter_df,
        x="ΔH",
        y="relative nvPM EIn",
        color="F/F00",
        hover_data=[c for c in ["Fuel", "Engine", "Campaign", "Thrust", "F/F00", "Hydrogen", "Ref Hydrogen", "ΔH"] if c in scatter_df.columns],
        color_continuous_scale="Viridis",
        opacity=0.8,
        title="nvPM EIn vs change in hydrogen content from reference fuel (color = thrust)",
    )
    fig_scatter.update_traces(marker=dict(size=9, line=dict(width=0.4, color="black")))
    fig_scatter.update_layout(
        xaxis_title="Change in hydrogen content from reference fuel, ΔH = H_fuel − H_ref (%)",
        yaxis_title="relative nvPM EIn number",
        coloraxis_colorbar_title="F/F00",
        margin=dict(l=40, r=20, t=60, b=50),
    )

    ycols = []
    if "relative nvPM EIn" in df.columns:
        ycols.append("relative nvPM EIn")
    if "relative mBC" in df.columns:
        ycols.append("relative mBC")

    # ---- (3) 3D surface/contour over (ΔH, F/F00) ----
    # Approach: fit one smooth 2D regression surface (poly2) on log(Relative EI).
    # Aromatics bins are intentionally not used for these bottom EIn/mBC plots.

    def _fit_poly2_surface(H: np.ndarray, F: np.ndarray, y: np.ndarray):
        # model: log(y) = c0 + c1 H + c2 F + c3 H^2 + c4 F^2 + c5 H*F
        X = np.column_stack(
            [
                np.ones_like(H),
                H,
                F,
                H**2,
                F**2,
                H * F,
            ]
        )
        beta, *_ = np.linalg.lstsq(X, np.log(y), rcond=None)
        return beta

    def _predict_poly2(beta: np.ndarray, H: np.ndarray, F: np.ndarray):
        X = np.column_stack([np.ones_like(H), H, F, H**2, F**2, H * F])
        return np.exp(X @ beta)

    # Build one 3D figure per metric (EIn/EIm)
    figs_3d: dict[str, go.Figure] = {}

    arom_col = None

    for metric in ycols:
        d = df[["ΔH", "F/F00", metric] + (["Aromatics"] if "Aromatics" in df.columns else [])].copy()
        d = d[np.isfinite(d[metric]) & np.isfinite(d["ΔH"]) & np.isfinite(d["F/F00"])].copy()
        # avoid log(0)
        d = d[d[metric] > 0]
        if len(d) < 12:
            continue

        if arom_col is None:
            # single surface
            beta = _fit_poly2_surface(d["ΔH"].to_numpy(float), d["F/F00"].to_numpy(float), d[metric].to_numpy(float))
            Hgrid = np.linspace(d["ΔH"].min(), d["ΔH"].max(), 40)
            Fgrid = np.linspace(d["F/F00"].min(), d["F/F00"].max(), 40)
            Hg, Fg = np.meshgrid(Hgrid, Fgrid)
            Z = _predict_poly2(beta, Hg.ravel(), Fg.ravel()).reshape(Hg.shape)

            fig3d = go.Figure()
            fig3d.add_trace(
                go.Surface(
                    x=Hg,
                    y=Fg,
                    z=Z,
                    colorscale="Viridis",
                    opacity=0.85,
                    name="surface",
                    colorbar=dict(title=f"Fitted {metric}"),
                )
            )
            fig3d.add_trace(
                go.Scatter3d(
                    x=d["ΔH"],
                    y=d["F/F00"],
                    z=d[metric],
                    mode="markers",
                    marker=dict(size=4, color="black", opacity=0.6),
                    name="data",
                )
            )
            fig3d.update_layout(
                title=f"{metric}: fitted surface over ΔH × F/F00",
                scene=dict(
                    xaxis_title="ΔH = H_fuel − H_ref (%)",
                    yaxis_title="F/F00",
                    zaxis_title=metric,
                    domain=dict(x=[0.0, 0.98], y=[0.0, 0.98]),
                ),
                autosize=True,
                height=820,
                margin=dict(l=0, r=0, t=35, b=0),
            )
            figs_3d[metric] = fig3d
        else:
            # frames by aromatics bin
            d = d[np.isfinite(d["Aromatics"])].copy()
            if len(d) < 12:
                continue

            # quantile bins (same as above but recompute on d)
            arom_vals = d["Aromatics"].to_numpy(float)
            qs = np.quantile(arom_vals, [0, 1 / 6, 2 / 6, 3 / 6, 4 / 6, 5 / 6, 1])
            qs = np.unique(qs)
            if len(qs) < 3:
                continue

            bins = list(zip(qs[:-1], qs[1:]))

            # common grids
            Hgrid = np.linspace(d["ΔH"].min(), d["ΔH"].max(), 35)
            Fgrid = np.linspace(d["F/F00"].min(), d["F/F00"].max(), 35)
            Hg, Fg = np.meshgrid(Hgrid, Fgrid)

            base = go.Figure()

            frames = []
            for lo, hi in bins:
                db = d[(d["Aromatics"] >= lo) & (d["Aromatics"] <= hi)].copy()
                if len(db) < 10:
                    continue
                beta = _fit_poly2_surface(
                    db["ΔH"].to_numpy(float),
                    db["F/F00"].to_numpy(float),
                    db[metric].to_numpy(float),
                )
                Z = _predict_poly2(beta, Hg.ravel(), Fg.ravel()).reshape(Hg.shape)

                frame_name = f"{lo:.2f}–{hi:.2f}%"
                frames.append(
                    go.Frame(
                        name=frame_name,
                        data=[
                            go.Surface(
                                x=Hg,
                                y=Fg,
                                z=Z,
                                colorscale="Viridis",
                                opacity=0.85,
                                colorbar=dict(title=f"Fitted {metric}"),
                            ),
                            go.Scatter3d(
                                x=db["ΔH"],
                                y=db["F/F00"],
                                z=db[metric],
                                mode="markers",
                                marker=dict(size=4, color="black", opacity=0.6),
                            ),
                        ],
                    )
                )

            if not frames:
                continue

            # init with first frame
            base.add_trace(frames[0].data[0])
            base.add_trace(frames[0].data[1])
            base.frames = frames

            slider_steps = []
            for fr in frames:
                slider_steps.append(
                    {
                        "method": "animate",
                        "label": fr.name,
                        "args": [[fr.name], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate"}],
                    }
                )

            base.update_layout(
                title=f"{metric}: fitted surface over ΔH × F/F00 (slider = aromatics bin)",
                scene=dict(xaxis_title="ΔH = H_fuel − H_ref (%)", yaxis_title="F/F00", zaxis_title=metric),
                margin=dict(l=0, r=0, t=50, b=0),
                sliders=[{"active": 0, "steps": slider_steps, "x": 0.05, "len": 0.9, "y": 0.02}],
            )
            figs_3d[metric] = base

    # ---- write a single HTML with both views (+ optional constrained-fit summary) ----
    out_html.parent.mkdir(parents=True, exist_ok=True)

    parts = []
    parts.append(fig_scatter.to_html(include_plotlyjs="cdn", full_html=False))
    for metric, fig3d in figs_3d.items():
        parts.append(fig3d.to_html(include_plotlyjs=False, full_html=False))

    def _img(name: str, label: str) -> str:
        if outdir is None:
            return ""
        p = outdir / name
        if not p.exists():
            return ""
        return (
            f"<div style=\"margin-top:12px\">"
            f"<div style=\"font-weight:600;margin:6px 0\">{label}</div>"
            f"<img src=\"{p.name}\" style=\"max-width:100%;height:auto;border:1px solid #eee\"/>"
            f"</div>"
        )

    diagnostics_table_html = ""
    param_popovers: dict[str, str] = {}
    if outdir is not None:
        table_csv_path = outdir / "ein_model_diagnostics_summary.csv"
        if table_csv_path.exists():
            import html as html_lib

            summary_df = pd.read_csv(table_csv_path)
            perf_cols = [c for c in ["display_name", "r2", "rmse", "mae", "n"] if c in summary_df.columns]
            performance_df = summary_df[perf_cols].rename(
                columns={
                    "display_name": "Function",
                    "r2": "R-squared",
                    "rmse": "Root Mean Square Error",
                    "mae": "Mean Absolute Error",
                    "n": "N",
                }
            )
            diagnostics_table_html = performance_df.to_html(
                index=False,
                float_format=lambda x: f"{x:.4g}",
                classes="performance-table",
                escape=False,
            )
            diagnostics_table_html = (
                diagnostics_table_html
                .replace(">R-squared<", "><span title=\"R-squared: fraction of variance in observed relative nvPM EIn explained by the model. Higher is better; 1 is perfect.\">R-squared</span><")
                .replace(">Root Mean Square Error<", "><span title=\"Root Mean Square Error (RMSE): typical prediction error in relative nvPM EIn, with larger errors penalized more. Lower is better.\">Root Mean Square Error</span><")
                .replace(">Mean Absolute Error<", "><span title=\"Mean Absolute Error (MAE): average absolute prediction error in relative nvPM EIn. Lower is better.\">Mean Absolute Error</span><")
                .replace(">N<", "><span title=\"N: number of data points used to fit/evaluate the model.\">N</span><")
            )

            metric_cols = {"model", "display_name", "r2", "rmse", "mae", "n"}
            for _, row in summary_df.iterrows():
                model_id = str(row.get("model", ""))
                lines = []
                for col in summary_df.columns:
                    if col in metric_cols or pd.isna(row[col]):
                        continue
                    try:
                        val = f"{float(row[col]):.4g}"
                    except Exception:
                        val = str(row[col])
                    lines.append(f"<li><b>{html_lib.escape(str(col))}</b>: {html_lib.escape(val)}</li>")
                param_popovers[model_id] = "".join(lines) if lines else "<li>No fitted parameters found.</li>"

    def _params(model_id: str) -> str:
        return param_popovers.get(model_id, "<li>Run diagnostics to populate fitted parameters.</li>")

    functions_explainer_html = f"""
  <div class="block function-section">
    <h3>Functions considered</h3>
    <p class="function-note">
      All functions first model <b>g(H,F) = relative nvPM EIn versus the 13.8% hydrogen baseline</b>, with
      <b>x = H − 13.8</b> and <b>F = Thrust / 100</b>. Experimental fuel/reference ratios are then predicted as
      <b>g(H<sub>fuel</sub>,F) / g(H<sub>ref</sub>,F)</b>.
    </p>

    <div class="function-grid">
      <div class="function-card">
        <h4>ICAO-family exponential</h4>
        <div class="equation">g(H,F) = exp[(αF + β)(H − 13.8)]</div>
        <p>Simple ICAO-style baseline correction. Thrust changes the hydrogen sensitivity.</p>
        <div class="param-popover"><b>Fitted parameters</b><ul>{_params('icao_family_exp')}</ul></div>
      </div>

      <div class="function-card">
        <h4>Mechanistic ICAO ratio</h4>
        <div class="equation">g(H,F) = exp[(aF² + bF + c)(H − 13.8)]</div>
        <p>Same baseline-ratio idea, but allows a curved/nonlinear thrust dependence.</p>
        <div class="param-popover"><b>Fitted parameters</b><ul>{_params('mechanistic_icao_ratio')}</ul></div>
      </div>

      <div class="function-card">
        <h4>Power-law exponential</h4>
        <div class="equation">g(H,F) = exp[(aF + b) · sign(x)|x|ᵖ]</div>
        <div class="sub-equation">x = H − 13.8</div>
        <p>Lets hydrogen response be nonlinear relative to the 13.8% baseline while preserving whether H is above or below baseline.</p>
        <div class="param-popover"><b>Fitted parameters</b><ul>{_params('power_law_exp')}</ul></div>
      </div>

      <div class="function-card">
        <h4>Saturating exponential</h4>
        <div class="equation">g(H,F) = exp{{-A(F)[1 − exp(−k(H − 13.8))]}}</div>
        <div class="sub-equation">A(F) &gt; 0, k &gt; 0</div>
        <p>Allows the nvPM reduction relative to 13.8% hydrogen to level off rather than changing indefinitely.</p>
        <div class="param-popover"><b>Fitted parameters</b><ul>{_params('saturating_exp')}</ul></div>
      </div>

      <div class="function-card">
        <h4>Log-polynomial</h4>
        <div class="equation">log[g(H,F)] = c₁x + c₂x² + c₃xF + c₄x²F + c₅xF²</div>
        <div class="sub-equation">x = H − 13.8; g(13.8,F)=1</div>
        <p>Flexible empirical surface anchored to the 13.8% baseline.</p>
        <div class="param-popover"><b>Fitted parameters</b><ul>{_params('log_poly2')}</ul></div>
      </div>

      <div class="function-card">
        <h4>Quadratic rational</h4>
        <div class="equation">g(H,F) = (1 − Ĥ)[(a + bF)Ĥ + 1]</div>
        <div class="sub-equation">Ĥ = (H − 13.8) / (H<sub>inf</sub> − 13.8)</div>
        <p>Shape-inspired hydrogen response with a finite high-hydrogen scale.</p>
        <div class="param-popover"><b>Fitted parameters</b><ul>{_params('quad_rational')}</ul></div>
      </div>

      <div class="function-card">
        <h4>Quadratic rational constrained</h4>
        <div class="equation">g(H,F) = (1 − Ĥ)[(a + bF)Ĥ + 1]</div>
        <div class="sub-equation">Ĥ = (H − 13.8) / (H<sub>inf</sub> − 13.8)</div>
        <p>Same equation as quadratic rational, but fitted with physical-shape guardrails. Hover for constraints and fitted parameters.</p>
        <div class="param-popover">
          <b>Constraints</b>
          <ul>
            <li><b>Scale constraint</b>: H<sub>inf</sub> must be larger than the largest observed hydrogen content and greater than 13.8%.</li>
            <li><b>Monotonicity constraint</b>: predicted baseline-relative nvPM EIn must not increase as H increases over the observed data range.</li>
            <li><b>Thrust-grid check</b>: monotonicity is checked across representative thrust values from F/F00 = 0.05 to 1.00.</li>
          </ul>
          <b>Fitted parameters</b><ul>{_params('quad_rational_constrained')}</ul>
        </div>
      </div>
    </div>
  </div>
"""

    parity_plot_html = f"""
  <div class=\"block\" style=\"padding:12px;border:1px solid #ddd;border-radius:8px;background:#fafafa\">
    <h3>EIn model diagnostics by function</h3>
    <p>Parity and residual plots are side-by-side with one shared Engine/Campaign legend. Diagnostics are generated by <code>nvpm_analysis/ein_model_diagnostics.py</code>.</p>
    {_img('ein_parity_all_models.png','Parity plots for all fitted functions')}
    {_img('ein_residuals_all_models.png','Residual plots for all fitted functions')}
    <h4>Model performance</h4>
    <div style=\"overflow-x:auto\">{diagnostics_table_html}</div>
  </div>
"""

    best_fit_html = ""
    if outdir is not None:
        import json

        best_summary_path = outdir / "ein_best_fit_bootstrap_summary.json"
        if best_summary_path.exists():
            s = json.loads(best_summary_path.read_text(encoding="utf-8"))
            best_model = s.get("best_model")

            panel_lightboxes = """
    <div id="panel-icao" class="lightbox"><a href="#" class="lightbox-close" aria-label="Close enlarged plot">×</a><img src="ein_hydrogen_bootstrap_icao_family_exp.png" alt="ICAO-Family Exponential" /></div>
    <div id="panel-mech-icao" class="lightbox"><a href="#" class="lightbox-close" aria-label="Close enlarged plot">×</a><img src="ein_hydrogen_bootstrap_mechanistic_icao_ratio.png" alt="Mechanistic ICAO Ratio" /></div>
    <div id="panel-power" class="lightbox"><a href="#" class="lightbox-close" aria-label="Close enlarged plot">×</a><img src="ein_hydrogen_bootstrap_power_law_exp.png" alt="Power-Law Exponential" /></div>
    <div id="panel-saturating" class="lightbox"><a href="#" class="lightbox-close" aria-label="Close enlarged plot">×</a><img src="ein_hydrogen_bootstrap_saturating_exp.png" alt="Saturating Exponential" /></div>
    <div id="panel-log-poly2" class="lightbox"><a href="#" class="lightbox-close" aria-label="Close enlarged plot">×</a><img src="ein_hydrogen_bootstrap_log_poly2.png" alt="Log-Polynomial (2nd Order)" /></div>
    <div id="panel-quad-rational" class="lightbox"><a href="#" class="lightbox-close" aria-label="Close enlarged plot">×</a><img src="ein_hydrogen_bootstrap_quad_rational.png" alt="Quadratic Rational" /></div>
    <div id="panel-quad-rational-constrained" class="lightbox"><a href="#" class="lightbox-close" aria-label="Close enlarged plot">×</a><img src="ein_hydrogen_bootstrap_quad_rational_constrained.png" alt="Quadratic Rational Constrained" /></div>
"""

            best_fit_html = f"""
  <div class=\"block\" style=\"padding:12px;border:1px solid #ddd;border-radius:8px;background:#fafafa\">
    <h3>Plotting fitted functions</h3>
    <p><b>Best fit:</b> {s.get('display_name', 'unknown')} ({s.get('selection_rule', 'lowest RMSE')}).
       R²={s.get('r2', float('nan')):.4g}, RMSE={s.get('rmse', float('nan')):.4g}, MAE={s.get('mae', float('nan')):.4g}, n={s.get('n', '')}.</p>
    <p style=\"margin-bottom:8px\"><b>Click an individual panel to enlarge only that model.</b> These curves show model-predicted relative nvPM EIn versus the 13.8% hydrogen baseline; experimental fuel/reference ratios are evaluated in the parity and residual plots above.</p>
    <div class=\"plot-click-wrap\">
      <img src=\"ein_all_models_hydrogen_bootstrap_bands.png\" alt=\"All model functions with bootstrap confidence bands\" />
      <a class=\"panel-hotspot panel-r1c1\" href=\"#panel-icao\" aria-label=\"Enlarge ICAO-Family Exponential panel\"></a>
      <a class=\"panel-hotspot panel-r1c2\" href=\"#panel-mech-icao\" aria-label=\"Enlarge Mechanistic ICAO Ratio panel\"></a>
      <a class=\"panel-hotspot panel-r1c3\" href=\"#panel-power\" aria-label=\"Enlarge Power-Law Exponential panel\"></a>
      <a class=\"panel-hotspot panel-r1c4\" href=\"#panel-saturating\" aria-label=\"Enlarge Saturating Exponential panel\"></a>
      <a class=\"panel-hotspot panel-r2c1\" href=\"#panel-log-poly2\" aria-label=\"Enlarge Log-Polynomial panel\"></a>
      <a class=\"panel-hotspot panel-r2c2\" href=\"#panel-quad-rational\" aria-label=\"Enlarge Quadratic Rational panel\"></a>
      <a class=\"panel-hotspot panel-r2c3\" href=\"#panel-quad-rational-constrained\" aria-label=\"Enlarge Quadratic Rational Constrained panel\"></a>
    </div>
    {panel_lightboxes}
    <p style=\"font-size:0.95em\"><b>How the 95% CI was computed:</b> for each model, fit once to the observed fuel/reference ratios using predictions g(H<sub>fuel</sub>,F)/g(H<sub>ref</sub>,F), compute residuals (observed − fitted), repeatedly resample those residuals with replacement, add them back to the fitted predictions to make synthetic datasets, refit the same model to each synthetic dataset, and predict the baseline-relative hydrogen-response curve g(H,F). At each hydrogen value, the band is the 2.5th to 97.5th percentile of those bootstrap predictions. The plotted curves are relative to the 13.8% hydrogen baseline and show several thrust levels.</p>
  </div>
"""

    html = """<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>nvPM interactive explorer</title>
  <style>
    body {{ font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; margin: 0; padding: 16px; }}
    .block {{ margin-bottom: 28px; }}
    .function-section {{ padding: 14px; border: 1px solid #ddd; border-radius: 8px; background: #fafafa; }}
    .function-note {{ margin-bottom: 14px; }}
    .function-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(310px, 1fr)); gap: 12px; }}
    .function-card {{ position: relative; background: white; border: 1px solid #e2e2e2; border-radius: 10px; padding: 12px; }}
    .function-card:hover {{ border-color: #9db7ff; box-shadow: 0 8px 30px rgba(0,0,0,0.12); }}
    .function-card h4 {{ margin: 0 0 8px; }}
    .equation {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 15px; background: #f3f6ff; border: 1px solid #dfe7ff; border-radius: 7px; padding: 9px; overflow-x: auto; white-space: nowrap; }}
    .sub-equation {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 13px; color: #555; margin-top: 6px; }}
    .function-card p {{ margin: 9px 0 0; color: #333; }}
    .constraint-list {{ margin: 8px 0 0; padding-left: 18px; color: #333; font-size: 13.5px; }}
    .constraint-list li {{ margin: 4px 0; }}
    .param-popover {{ display: none; position: absolute; left: 12px; right: 12px; top: calc(100% - 4px); z-index: 50; background: #111827; color: white; border-radius: 9px; padding: 10px 12px; box-shadow: 0 14px 45px rgba(0,0,0,0.28); font-size: 13px; }}
    .param-popover ul {{ margin: 6px 0 0; padding-left: 18px; }}
    .param-popover li {{ margin: 2px 0; }}
    .function-card:hover .param-popover {{ display: block; }}
    .performance-table {{ border-collapse: collapse; width: 100%; background: white; }}
    .performance-table th, .performance-table td {{ border: 1px solid #ddd; padding: 7px 9px; text-align: right; }}
    .performance-table th:first-child, .performance-table td:first-child {{ text-align: left; }}
    .performance-table th {{ background: #f3f6ff; }}
    .performance-table th span[title] {{ cursor: help; text-decoration: underline dotted #667; text-underline-offset: 3px; }}
    .surface-block .plotly-graph-div {{ min-height: 760px; }}
    .plot-click-wrap {{ position: relative; display: block; max-width: 100%; }}
    .plot-click-wrap > img {{ width: 100%; height: auto; display: block; border: 1px solid #eee; }}
    .panel-hotspot {{ position: absolute; display: block; cursor: zoom-in; border-radius: 8px; transition: background 120ms ease, outline 120ms ease; }}
    .panel-hotspot:hover {{ background: rgba(255, 230, 128, 0.16); outline: 2px solid rgba(212, 175, 55, 0.75); }}
    .panel-r1c1 {{ left: 6%; top: 14%; width: 20%; height: 30%; }}
    .panel-r1c2 {{ left: 27%; top: 14%; width: 20%; height: 30%; }}
    .panel-r1c3 {{ left: 48%; top: 14%; width: 20%; height: 30%; }}
    .panel-r1c4 {{ left: 69%; top: 14%; width: 20%; height: 30%; }}
    .panel-r2c1 {{ left: 16%; top: 51%; width: 20%; height: 30%; }}
    .panel-r2c2 {{ left: 38%; top: 51%; width: 20%; height: 30%; }}
    .panel-r2c3 {{ left: 60%; top: 51%; width: 20%; height: 30%; }}
    .lightbox {{ display:none; position:fixed; inset:0; z-index:9999; background:rgba(0,0,0,0.82); padding:28px; box-sizing:border-box; align-items:center; justify-content:center; }}
    .lightbox:target {{ display:flex; }}
    .lightbox img {{ max-width:96vw; max-height:92vh; background:white; border-radius:8px; box-shadow:0 20px 80px rgba(0,0,0,0.5); }}
    .lightbox-close {{ position:fixed; top:14px; right:24px; color:white; font-size:42px; line-height:1; text-decoration:none; font-weight:700; }}
  </style>
</head>
<body>
  <h2>nvPM interactive explorer</h2>
  <p>Scatter: x-axis is change in hydrogen content from the reference fuel (ΔH = H_fuel − H_ref), y-axis is relative nvPM EIn number, and point color is thrust (F/F00). Hover over each point for fuel, engine, and campaign.<br/>
     3D surface: ΔH × F/F00 surface with no aromatics binning. In the relative nvPM EIn and mBC 3D plots, the color bar shows the fitted relative EI value on the surface.</p>
  <div class="block">{scatter}</div>
  {functions_explainer}
  {parity_plots}
  {best_fit}
  {surfaces}
</body>
</html>
"""

    surfaces_html = "\n".join([f'<div class="block surface-block">{p}</div>' for p in parts[1:]])
    out_html.write_text(
        html.format(
            scatter=parts[0],
            surfaces=surfaces_html,
            functions_explainer=functions_explainer_html,
            parity_plots=parity_plot_html,
            best_fit=best_fit_html,
        ),
        encoding="utf-8",
    )


# ------------------------- main -------------------------

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--excel", required=True)
    ap.add_argument("--sheet", default="PM Emissions")
    ap.add_argument("--outdir", default="nvpm_analysis_outputs")
    ap.add_argument("--nboot", type=int, default=1000)
    args = ap.parse_args()

    excel = Path(args.excel).expanduser()
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    df = pd.read_excel(excel, sheet_name=args.sheet)

    # interactive
    build_interactive(df, outdir / "nvpm_interactive.html", outdir=outdir)

    # fit EIn and EIm (quadratic) if columns exist
    df = df.copy()
    df["F"] = df["Thrust"] / 100.0

    def _do_fit(ycol: str, tag: str):
        mask = np.isfinite(df[ycol]) & np.isfinite(df["Hydrogen"]) & np.isfinite(df["Ref Hydrogen"]) & np.isfinite(df["F"])
        d = df.loc[mask]
        y = d[ycol].to_numpy(float)
        Hf = d["Hydrogen"].to_numpy(float)
        Hr = d["Ref Hydrogen"].to_numpy(float)
        F = d["F"].to_numpy(float)

        fit = fit_quadratic(y, Hf, Hr, F, initial=(-1.3, 1.98, 15.92), n_boot=args.nboot)

        # ICAO R2 for comparison
        icao = icao_h_model(Hf, Hr, F, which=tag)
        r2_icao = r2_score(y, icao)

        # save parity plot with bootstrap band
        import matplotlib.pyplot as plt

        vmin = float(np.nanmin(np.r_[y, fit.yhat]))
        vmax = float(np.nanmax(np.r_[y, fit.yhat]))

        sort = np.argsort(fit.yhat)
        plt.figure(figsize=(6.5, 6.5))
        plt.fill_between(fit.yhat[sort], fit.ci_lower[sort], fit.ci_upper[sort], color="lightgray", alpha=0.8, label="bootstrap 95% CI")
        plt.scatter(y, fit.yhat, s=45, alpha=0.8, edgecolor="k", linewidth=0.3)
        plt.plot([vmin, vmax], [vmin, vmax], "k--", lw=1.5)
        plt.gca().set_aspect("equal", adjustable="box")
        plt.xlim(vmin, vmax)
        plt.ylim(vmin, vmax)
        plt.xlabel(f"Experimental {ycol}")
        plt.ylabel(f"Quadratic fit prediction")
        plt.title(f"{tag}: quadratic fit parity\nR²={fit.r2:.3f} | ICAO R²={r2_icao:.3f}")
        plt.legend(loc="lower right")
        plt.tight_layout()
        plt.savefig(outdir / f"{tag}_parity_bootstrap.png", dpi=200)
        plt.close()

        # residual plot
        plt.figure(figsize=(6.5, 4.5))
        plt.scatter(fit.yhat, fit.residuals, s=45, alpha=0.8, edgecolor="k", linewidth=0.3)
        plt.axhline(0, color="k", ls="--", lw=1.2)
        plt.xlabel("Prediction")
        plt.ylabel("Residual (y - yhat)")
        plt.title(f"{tag}: residuals (quadratic fit)")
        plt.tight_layout()
        plt.savefig(outdir / f"{tag}_residuals.png", dpi=200)
        plt.close()

        print(f"\n[{tag}] Quadratic fit")
        print(f"  params: a={fit.params[0]:.4g}, b={fit.params[1]:.4g}, H_inf={fit.params[2]:.4g}")
        print(f"  R2(quadratic)={fit.r2:.4f}")
        print(f"  R2(ICAO exp)={r2_icao:.4f}")

    if "relative nvPM EIn" in df.columns:
        _do_fit("relative nvPM EIn", "EIn")
    if "relative mBC" in df.columns:
        _do_fit("relative mBC", "EIm")


if __name__ == "__main__":
    main()
