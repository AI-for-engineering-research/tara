"""Generate the website schematic SVG: conventional vs low-aromatic fuel.

This creates a light, two-panel schematic:
  Engine -> soot (nvPM) -> ice crystals -> contrail RF

Outputs:
  assets/images/soot_low_aromatic_vs_conventional.svg

Run:
  python3 nvpm_analysis/make_soot_contrail_schematic.py

Notes:
- Uses matplotlib only (no seaborn).
- Intentionally *conceptual* (directional), not quantitative.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


# ---------- helpers ----------

def snowflake(ax, x, y, s=0.06, color="#1d4ed8", alpha=0.55, lw=1.2):
    """Simple 6-arm snowflake icon."""
    for ang in [0, np.pi / 2, np.pi / 4, -np.pi / 4]:
        dx = s * np.cos(ang)
        dy = s * np.sin(ang)
        ax.plot([x - dx, x + dx], [y - dy, y + dy], color=color, alpha=alpha, lw=lw, solid_capstyle="round")
    ax.add_patch(patches.Circle((x, y), radius=s * 0.18, facecolor=color, edgecolor="none", alpha=alpha))


def draw_engine(ax, X_ENGINE, Y_CENTER, scale=1.0):
    """Engine nacelle outline + nozzle + internal streamlines (no arrowheads).

    Styled after the code snippet you provided.
    """

    # geometry (scaled)
    x0 = X_ENGINE + 0.24 * scale
    x_fan = X_ENGINE + 0.72 * scale
    x_tail = X_ENGINE + 1.95 * scale

    r_inlet = 0.30 * scale
    r_max = 0.36 * scale
    r_tail = 0.28 * scale

    upper = np.array(
        [
            [x0, Y_CENTER + r_inlet],
            [x0 + 0.14 * scale, Y_CENTER + (r_inlet + 0.06 * scale)],
            [x_fan - 0.06 * scale, Y_CENTER + (r_max - 0.01 * scale)],
            [x_fan, Y_CENTER + r_max],
            [x_fan + 0.40 * scale, Y_CENTER + 0.33 * scale],
            [x_tail - 0.25 * scale, Y_CENTER + 0.30 * scale],
            [x_tail, Y_CENTER + r_tail],
        ]
    )
    lower = upper.copy()
    lower[:, 1] = 2 * Y_CENTER - lower[:, 1]
    profile = np.vstack([upper, lower[::-1]])

    edge = "#7F8C8D"
    ax.add_patch(
        patches.Polygon(
            profile,
            closed=True,
            facecolor="white",
            edgecolor=edge,
            linewidth=2.2,
            joinstyle="round",
        )
    )

    # nozzle
    ax.add_patch(
        patches.Polygon(
            [
                (x_tail - 0.02 * scale, Y_CENTER - 0.22 * scale),
                (x_tail + 0.34 * scale, Y_CENTER - 0.12 * scale),
                (x_tail + 0.34 * scale, Y_CENTER + 0.12 * scale),
                (x_tail - 0.02 * scale, Y_CENTER + 0.22 * scale),
            ],
            closed=True,
            facecolor="white",
            edgecolor=edge,
            linewidth=2.0,
            joinstyle="round",
        )
    )

    # streamlines
    air_color = "#2C3E50"
    arrow_alpha = 0.28
    lw = 2.0

    for yoff, bulge in [(0.0, 0.0), (0.10 * scale, 0.16 * scale), (-0.10 * scale, -0.16 * scale)]:
        # piecewise curve points
        p0 = (x0 + 0.06 * scale, Y_CENTER + yoff)
        p1 = (x_fan - 0.05 * scale, Y_CENTER + yoff + 0.70 * bulge)
        cA = (x0 + 0.25 * scale, Y_CENTER + yoff + 0.20 * bulge)

        p2 = (x_fan + 0.55 * scale, Y_CENTER + yoff + 0.45 * bulge)
        cB = (x_fan + 0.18 * scale, Y_CENTER + yoff + 0.85 * bulge)

        p3 = (x_tail + 0.26 * scale, Y_CENTER + yoff + 0.05 * bulge)
        cC = (x_tail - 0.02 * scale, Y_CENTER + yoff + 0.18 * bulge)

        p4 = (x_tail + 0.85 * scale, Y_CENTER + yoff + 0.02 * bulge)
        cD = (x_tail + 0.45 * scale, Y_CENTER + yoff + 0.08 * bulge)

        def quad_bezier(P0, C, P1, n=40):
            t = np.linspace(0, 1, n)
            x = (1 - t) ** 2 * P0[0] + 2 * (1 - t) * t * C[0] + t**2 * P1[0]
            y = (1 - t) ** 2 * P0[1] + 2 * (1 - t) * t * C[1] + t**2 * P1[1]
            return x, y

        for A, B, C in [(p0, p1, cA), (p1, p2, cB), (p2, p3, cC), (p3, p4, cD)]:
            x, y = quad_bezier(A, C, B)
            ax.plot(x, y, color=air_color, alpha=arrow_alpha, lw=lw, solid_capstyle="round")

    ax.text(X_ENGINE + 1.10 * scale, Y_CENTER - 0.58 * scale, "ENGINE", fontsize=9.5, ha="center", va="center", fontweight="bold", color="#2C3E50")


def panel(ax, x0, y0, w, h, title):
    ax.add_patch(
        patches.FancyBboxPatch(
            (x0, y0),
            w,
            h,
            boxstyle="round,pad=0.02,rounding_size=0.18",
            facecolor="white",
            edgecolor="#e2e8f0",
            linewidth=1.5,
        )
    )
    ax.text(x0 + 0.30, y0 + h - 0.38, title, fontsize=15, fontweight=800, color="#0b1220", ha="left", va="center")


def main():
    out = Path("assets/images/soot_low_aromatic_vs_conventional.svg")
    out.parent.mkdir(parents=True, exist_ok=True)

    fig = plt.figure(figsize=(16, 5.9), facecolor="white")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 5.9)
    ax.axis("off")

    # header
    ax.text(
        0.8,
        5.25,
        "Low aromatic jet fuel → lower soot → fewer ice crystals → lower contrail RF",
        fontsize=24,
        fontweight=900,
        color="#0b1220",
        ha="left",
        va="center",
    )
    ax.text(0.8, 4.93, "Conceptual schematic (directional, not quantitative)", fontsize=13.5, color="#475569", ha="left", va="center")

    # panels
    panel(ax, 0.8, 0.8, 7.0, 3.75, "Conventional jet fuel")
    panel(ax, 8.2, 0.8, 7.0, 3.75, "Low aromatic jet fuel")

    # step labels
    step_color = "#64748b"
    ax.text(1.10, 4.05, "ENGINE", fontsize=10.5, fontweight=700, color=step_color, ha="left")
    ax.text(3.70, 4.05, "SOOT (nvPM)", fontsize=10.5, fontweight=700, color=step_color, ha="left")
    ax.text(5.25, 4.05, "ICE CRYSTALS", fontsize=10.5, fontweight=700, color=step_color, ha="left")
    ax.text(6.62, 4.05, "CONTRAIL RF", fontsize=10.5, fontweight=700, color=step_color, ha="left")

    ax.text(8.50, 4.05, "ENGINE", fontsize=10.5, fontweight=700, color=step_color, ha="left")
    ax.text(11.10, 4.05, "SOOT (nvPM)", fontsize=10.5, fontweight=700, color=step_color, ha="left")
    ax.text(12.65, 4.05, "ICE CRYSTALS", fontsize=10.5, fontweight=700, color=step_color, ha="left")
    ax.text(14.02, 4.05, "CONTRAIL RF", fontsize=10.5, fontweight=700, color=step_color, ha="left")

    # engine drawings
    draw_engine(ax, X_ENGINE=0.95, Y_CENTER=2.82, scale=1.55)
    draw_engine(ax, X_ENGINE=8.35, Y_CENTER=2.82, scale=1.55)

    # connectors (simple lines)
    for xA, xB in [(3.10, 3.75), (4.85, 5.25), (6.10, 6.62)]:
        ax.plot([xA, xB], [2.82, 2.82], color="#94a3b8", lw=2, alpha=0.55)
    for xA, xB in [(10.50, 11.15), (12.25, 12.65), (13.90, 14.02)]:
        ax.plot([xA, xB], [2.82, 2.82], color="#94a3b8", lw=2, alpha=0.55)

    # soot dots
    rng = np.random.default_rng(0)
    # conventional: more
    for _ in range(12):
        ax.add_patch(
            patches.Circle(
                (3.95 + rng.normal(0, 0.25), 2.82 + rng.normal(0, 0.22)),
                radius=rng.uniform(0.035, 0.065),
                facecolor="#0b1220",
                edgecolor="none",
                alpha=0.70,
            )
        )
    # low aromatic: fewer
    for _ in range(5):
        ax.add_patch(
            patches.Circle(
                (11.35 + rng.normal(0, 0.22), 2.82 + rng.normal(0, 0.18)),
                radius=rng.uniform(0.030, 0.052),
                facecolor="#0b1220",
                edgecolor="none",
                alpha=0.50,
            )
        )

    # ice crystals
    # conventional: more
    for (x, y, s) in [(5.35, 3.05, 0.085), (5.70, 2.85, 0.07), (6.00, 3.00, 0.075), (6.25, 2.75, 0.06), (5.90, 2.55, 0.06), (5.55, 2.55, 0.055)]:
        snowflake(ax, x, y, s=s)

    # low aromatic: fewer
    for (x, y, s) in [(12.75, 2.95, 0.07), (13.10, 2.75, 0.055), (13.45, 2.90, 0.06)]:
        snowflake(ax, x, y, s=s, alpha=0.40)

    # contrail ribbons
    ax.plot([5.15, 7.35], [1.85, 1.70], color="#93c5fd", lw=24, alpha=0.22, solid_capstyle="round")
    ax.plot([5.15, 7.35], [1.92, 1.78], color="#93c5fd", lw=9, alpha=0.12, solid_capstyle="round")

    ax.plot([12.55, 14.65], [1.85, 1.75], color="#93c5fd", lw=20, alpha=0.12, solid_capstyle="round")
    ax.plot([12.55, 14.65], [1.92, 1.82], color="#93c5fd", lw=8, alpha=0.07, solid_capstyle="round")

    # RF badges
    ax.add_patch(
        patches.FancyBboxPatch(
            (6.75, 3.25),
            0.72,
            0.28,
            boxstyle="round,pad=0.02,rounding_size=0.15",
            facecolor="#fee2e2",
            edgecolor="#fecaca",
            linewidth=1.2,
        )
    )
    ax.text(7.11, 3.39, "higher", fontsize=11, fontweight=800, color="#0b1220", ha="center", va="center")

    ax.add_patch(
        patches.FancyBboxPatch(
            (14.15, 3.25),
            0.72,
            0.28,
            boxstyle="round,pad=0.02,rounding_size=0.15",
            facecolor="#dcfce7",
            edgecolor="#bbf7d0",
            linewidth=1.2,
        )
    )
    ax.text(14.51, 3.39, "lower", fontsize=11, fontweight=800, color="#0b1220", ha="center", va="center")

    # footer note
    ax.text(0.8, 0.38, "Engine outline and streamlines are generated from code; dots/flakes indicate direction only.", fontsize=11.5, color="#64748b", ha="left")

    fig.savefig(out, format="svg")
    plt.close(fig)
    print(f"Wrote: {out}")


if __name__ == "__main__":
    main()
