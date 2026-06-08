import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Wedge, FancyArrowPatch
import numpy as np

# Create figure (left → right layout)
# Give a bit more vertical room so all callouts fit cleanly
fig, ax = plt.subplots(1, 1, figsize=(16, 6.2))
ax.set_xlim(0, 16)
ax.set_ylim(0, 6.2)
ax.axis('off')

# Deterministic layout randomness
np.random.seed(42)

# Layout anchors
Y_CENTER = 2.75
# Put stage labels closer to the diagram
STAGE_Y = 0.25

# X positions for stages
X_ENGINE = 1.2
X_HOT = 4.2
X_MIX = 7.2
X_ICE = 10.2
X_CONTRAIL = 13.1

# Helper: right-pointing arrow between stages
def stage_arrow(x0, x1, y=Y_CENTER, color='#34495E'):
    arr = FancyArrowPatch((x0, y), (x1, y), arrowstyle='->',
                         mutation_scale=26, linewidth=2.5, color=color)
    ax.add_patch(arr)
    return arr

# Color scheme
color_engine = '#FF6B35'
color_soot = '#2C3E50'
color_water = '#3498DB'
color_ice = '#ECF0F1'
color_contrail = '#FFFFFF'
color_ambient = '#87CEEB'

# Background - ambient air
ambient = patches.Rectangle((0, 0), 16, 6.2, linewidth=2,
                            edgecolor='#34495E', facecolor='#D6EAF8', alpha=0.3)
ax.add_patch(ambient)

# Add temperature label
# Ambient label (keep above other callouts)
ax.text(15.6, 5.12, 'Ambient Air\nT ≈ -40°C to -60°C',
        fontsize=10, ha='right', va='top', style='italic',
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.85))

# ============ STAGE 1: ENGINE (streamlined nacelle outline) ============
# Streamlined axisymmetric nacelle: rounded inlet lip, max diameter near fan face,
# and a gradually tapered afterbody.

# Build a smooth upper/lower profile using control points, then fill.
# (Simple geometric outline; no internal components.)

x0 = X_ENGINE + 0.24          # inlet x
x_fan = X_ENGINE + 0.72       # max diameter near fan face
x_tail = X_ENGINE + 1.95      # aft end (shorter)

# Overall wider diameter with less variation
r_inlet = 0.30
r_max = 0.36
r_tail = 0.28

# Upper surface control points (x, y)
upper = np.array([
    [x0,           Y_CENTER + r_inlet],
    [x0 + 0.14,    Y_CENTER + (r_inlet + 0.06)],
    [x_fan - 0.06, Y_CENTER + (r_max - 0.01)],
    [x_fan,        Y_CENTER + r_max],
    [x_fan + 0.40, Y_CENTER + 0.33],
    [x_tail - 0.25, Y_CENTER + 0.30],
    [x_tail,       Y_CENTER + r_tail],
])
# Lower surface (mirror)
lower = upper.copy()
lower[:, 1] = 2 * Y_CENTER - lower[:, 1]

# Create polygon (upper forward->aft, then lower aft->forward)
profile = np.vstack([upper, lower[::-1]])
ax.add_patch(patches.Polygon(profile, closed=True,
                             facecolor='white', edgecolor='#7F8C8D',
                             linewidth=2.2, joinstyle='round'))

# Nozzle (exhaust) at the aft end (slight taper)
ax.add_patch(patches.Polygon([
    (x_tail - 0.02, Y_CENTER - 0.22),
    (x_tail + 0.34, Y_CENTER - 0.12),
    (x_tail + 0.34, Y_CENTER + 0.12),
    (x_tail - 0.02, Y_CENTER + 0.22),
], closed=True, facecolor='white', edgecolor='#7F8C8D', linewidth=2.0, joinstyle='round'))

# Airflow arrows (skinny, semi-transparent, inside the nacelle)
# Multiple connected segments; upper/lower paths expand then contract.
air_color = '#2C3E50'
arrow_alpha = 0.45
ms = 14
arrow_lw = 2.2

# Helper to add a connected curved arrow segment (quadratic Bezier)
def curved_segment(p0, ctrl, p1):
    path = patches.Path([p0, ctrl, p1],
                        [patches.Path.MOVETO,
                         patches.Path.CURVE3,
                         patches.Path.CURVE3])
    ax.add_patch(FancyArrowPatch(
        path=path,
        arrowstyle='->',
        mutation_scale=ms,
        linewidth=arrow_lw,
        color=air_color,
        alpha=arrow_alpha,
        capstyle='round',
        joinstyle='round'
    ))

# Define three streamlines entirely within the nacelle profile
for yoff, bulge in [(0.0, 0.0), (0.10, 0.16), (-0.10, -0.16)]:
    # Segment A: inlet -> fan face (slight outward)
    p0 = (x0 + 0.06, Y_CENTER + yoff)
    p1 = (x_fan - 0.05, Y_CENTER + yoff + 0.70 * bulge)
    cA = (x0 + 0.25, Y_CENTER + yoff + 0.20 * bulge)

    # Segment B: fan face -> mid body
    p2 = (x_fan + 0.55, Y_CENTER + yoff + 0.45 * bulge)
    cB = (x_fan + 0.18, Y_CENTER + yoff + 0.85 * bulge)

    # Segment C: mid body -> nozzle exit (stay within nozzle)
    p3 = (x_tail + 0.26, Y_CENTER + yoff + 0.05 * bulge)
    cC = (x_tail - 0.02, Y_CENTER + yoff + 0.18 * bulge)

    # Segment D: after nozzle (jet continues downstream)
    p4 = (x_tail + 0.85, Y_CENTER + yoff + 0.02 * bulge)
    cD = (x_tail + 0.45, Y_CENTER + yoff + 0.08 * bulge)

    curved_segment(p0, cA, p1)
    curved_segment(p1, cB, p2)
    curved_segment(p2, cC, p3)
    curved_segment(p3, cD, p4)

# Label
ax.text(X_ENGINE + 1.15, Y_CENTER - 0.62, 'ENGINE',
        fontsize=9.5, ha='center', va='center', fontweight='bold', color='#2C3E50')


# Stage label (bottom)
ax.text(X_ENGINE + 1.4, STAGE_Y, 'STAGE 1\nEngine', fontsize=9.5,
        ha='center', va='center', fontweight='bold', color='#2C3E50')


# ============ STAGE 2: HOT EXHAUST & SOOT ============
ax.text(X_HOT + 0.7, STAGE_Y, 'STAGE 2\nHot Exhaust + Soot', fontsize=9.5,
        ha='center', va='center', fontweight='bold', color='#2C3E50')

# Draw expanding plume (horizontal)
plume = patches.Polygon([
    (X_HOT - 0.2, Y_CENTER - 0.35),
    (X_HOT + 1.2, Y_CENTER - 0.85),
    (X_HOT + 2.5, Y_CENTER - 0.55),
    (X_HOT + 2.5, Y_CENTER + 0.55),
    (X_HOT + 1.2, Y_CENTER + 0.85),
    (X_HOT - 0.2, Y_CENTER + 0.35),
], closed=True, facecolor=color_engine, alpha=0.30,
   edgecolor='#E74C3C', linewidth=2)
ax.add_patch(plume)

# Soot particles (black dots)
for _ in range(26):
    x = np.random.uniform(X_HOT + 0.2, X_HOT + 2.2)
    y = np.random.uniform(Y_CENTER - 0.6, Y_CENTER + 0.6)
    ax.add_patch(Circle((x, y), 0.06, color=color_soot, alpha=0.85))

ax.text(X_HOT + 1.2, Y_CENTER + 1.3,
        'Soot particles (BC)\n● Diameter: 10–100 nm',
        fontsize=9, ha='center', style='italic',
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.75))


# ============ STAGE 3: MIXING ZONE ============
ax.text(X_MIX + 0.7, STAGE_Y, 'STAGE 3\nMixing + Cooling', fontsize=9.5,
        ha='center', va='center', fontweight='bold', color='#2C3E50')

mixing_zone = FancyBboxPatch((X_MIX - 0.1, Y_CENTER - 0.75), 2.6, 1.5,
                            boxstyle="round,pad=0.06",
                            edgecolor=color_water, facecolor=color_water,
                            linewidth=2, alpha=0.22)
ax.add_patch(mixing_zone)

# Water vapor symbols (~)
for _ in range(18):
    x = np.random.uniform(X_MIX + 0.1, X_MIX + 2.2)
    y = np.random.uniform(Y_CENTER - 0.6, Y_CENTER + 0.6)
    ax.text(x, y, '~', fontsize=15, color=color_water, alpha=0.55)

# Soot particles still visible
for _ in range(12):
    x = np.random.uniform(X_MIX + 0.1, X_MIX + 2.2)
    y = np.random.uniform(Y_CENTER - 0.6, Y_CENTER + 0.6)
    ax.add_patch(Circle((x, y), 0.05, color=color_soot, alpha=0.65))

ax.text(X_MIX + 1.2, Y_CENTER + 1.25, 'RHᵢ > 100%\n(supersaturation)',
        fontsize=9, ha='center', style='italic',
        bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))


# ============ STAGE 4: ICE NUCLEATION ============
ax.text(X_ICE + 0.7, STAGE_Y, 'STAGE 4\nIce Nucleation', fontsize=9.5,
        ha='center', va='center', fontweight='bold', color='#2C3E50')

ice_zone = FancyBboxPatch((X_ICE - 0.1, Y_CENTER - 0.75), 2.6, 1.5,
                         boxstyle="round,pad=0.06",
                         edgecolor='#9B59B6', facecolor='#9B59B6',
                         linewidth=2, alpha=0.16)
ax.add_patch(ice_zone)

# Ice crystals forming
for _ in range(10):
    x = np.random.uniform(X_ICE + 0.1, X_ICE + 2.2)
    y = np.random.uniform(Y_CENTER - 0.55, Y_CENTER + 0.55)
    ax.text(x, y, '❄', fontsize=16, color='#3498DB', alpha=0.85)

ax.text(X_ICE + 1.2, Y_CENTER + 1.25,
        'Ice crystals form\naround BC nuclei\n(1–10 μm)',
        fontsize=9, ha='center', style='italic',
        bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.85))


# ============ STAGE 5: VISIBLE CONTRAIL ============
ax.text(X_CONTRAIL + 0.8, STAGE_Y, 'STAGE 5\nVisible Contrail', fontsize=9.5,
        ha='center', va='center', fontweight='bold', color='#2C3E50')

# Contrail cloud (and persistence) drawn as a widening plume to the right
contrail_center_y = Y_CENTER

# Dense core
for dx in np.linspace(-0.2, 2.0, 8):
    ax.add_patch(Circle((X_CONTRAIL + dx, contrail_center_y), 0.26,
                        color=color_ice, edgecolor='#BDC3C7', linewidth=1.2, alpha=0.95))

# Spreading / persistence (wider, more diffuse further right)
for dx in np.linspace(2.2, 4.3, 12):
    r = 0.24 + 0.10 * (dx - 2.2)
    ax.add_patch(Circle((X_CONTRAIL + dx, contrail_center_y + np.random.uniform(-0.35, 0.35)),
                        r, color=color_ice, edgecolor='#95A5A6', linewidth=1, alpha=0.65))

# Some darker ice crystals
for _ in range(18):
    x = np.random.uniform(X_CONTRAIL - 0.1, X_CONTRAIL + 4.4)
    y = np.random.uniform(Y_CENTER - 0.55, Y_CENTER + 0.55)
    ax.add_patch(Circle((x, y), 0.055, color='#95A5A6', alpha=0.45))

# Keep contrail callout below ambient label; keep winds box inside canvas
ax.text(X_CONTRAIL + 1.95, Y_CENTER + 1.05,
        'VISIBLE CONTRAIL\n✦ τ > 0.1\n✦ 10⁶–10⁸ ice crystals/cm³\n✦ Persistent if RHᵢ > 100%',
        fontsize=9.5, ha='center', fontweight='bold',
        bbox=dict(boxstyle='round', facecolor='white', edgecolor='#27AE60',
                 linewidth=2, alpha=0.96))

ax.text(X_CONTRAIL + 3.0, 0.85,
        'Spreads with winds\nSublimes if RHᵢ < 100%',
        fontsize=9, ha='center', style='italic',
        bbox=dict(boxstyle='round', facecolor='#E8F8F5', alpha=0.95))

# Add side annotations with key information
info_box_text = (
    'KEY FACTORS:\n'
    '• Fuel aromatic content → soot emissions\n'
    '• Soot acts as ice nuclei\n'
    '• Lower aromatics → lower emissions\n'
    '• Climate impact via radiative forcing'
)
ax.text(0.45, 6.05, info_box_text, fontsize=8.5,
        bbox=dict(boxstyle='round', facecolor='#FFF9E6', alpha=0.92, pad=0.7),
        ha='left', va='top', family='monospace')

# Title
fig.suptitle('Aircraft Soot Emissions & Contrail Formation',
             fontsize=16, fontweight='bold', y=0.98)

plt.tight_layout()
plt.savefig('contrail_formation.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✓ Image saved as 'contrail_formation.png'")
plt.show()