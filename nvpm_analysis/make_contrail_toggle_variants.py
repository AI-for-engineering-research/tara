"""Make obvious low-aromatic variant of the contrail formation figure.

This is a pragmatic *presentation* edit for the website toggle.
It does NOT attempt scientific pixel-detection; instead it applies
controlled overlays in broad regions to make the difference obvious.

Outputs:
  assets/images/contrail_formation_conventional.png (copy if missing)
  assets/images/contrail_formation_low_aromatic.png

Run:
  python3 nvpm_analysis/make_contrail_toggle_variants.py

If the overlays miss the right areas on your specific figure, adjust
REGIONS below.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance


SRC = Path("assets/images/contrail_formation.png")
CONV = Path("assets/images/contrail_formation_conventional.png")
LOW = Path("assets/images/contrail_formation_low_aromatic.png")

# Regions are in pixel coordinates of the source PNG.
# Format: (x1, y1, x2, y2)
# These defaults are broad and intended to be "obvious".
REGIONS = {
    # right half tends to contain contrail plume / crystals
    "soot": (0, 0, 0, 0),
    "ice": (0, 0, 0, 0),
    "contrail": (0, 0, 0, 0),
}


def guess_regions(w: int, h: int):
    """Heuristic guesses for contrail figure layout."""
    # Most contrail schematics are left->right flow; use right-middle for contrail.
    soot = (int(0.52 * w), int(0.36 * h), int(0.74 * w), int(0.72 * h))
    ice = (int(0.68 * w), int(0.22 * h), int(0.96 * w), int(0.62 * h))
    contrail = (int(0.52 * w), int(0.18 * h), int(0.98 * w), int(0.55 * h))
    return soot, ice, contrail


def white_wash(im: Image.Image, box, alpha=0.55):
    overlay = Image.new("RGBA", im.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)
    draw.rounded_rectangle(box, radius=26, fill=(255, 255, 255, int(255 * alpha)))
    return Image.alpha_composite(im, overlay)


def draw_thinner_contrail(im: Image.Image, box):
    """Fade existing contrail region and draw a thinner new ribbon."""
    x1, y1, x2, y2 = box

    # Step 1: fade the region substantially so the old thick contrail is subdued.
    im = white_wash(im, box, alpha=0.35)

    overlay = Image.new("RGBA", im.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    # New contrail line: thinner, lighter blue-white
    mid_y = int((y1 + y2) / 2)
    # gentle upward slope
    p0 = (x1 + int(0.02 * (x2 - x1)), mid_y + int(0.10 * (y2 - y1)))
    p1 = (x1 + int(0.55 * (x2 - x1)), mid_y - int(0.05 * (y2 - y1)))
    p2 = (x2 - int(0.02 * (x2 - x1)), mid_y - int(0.08 * (y2 - y1)))

    # draw multiple strokes for soft ribbon
    for w, a in [(18, 40), (10, 55), (4, 75)]:
        draw.line([p0, p1, p2], fill=(147, 197, 253, a), width=w, joint="curve")

    return Image.alpha_composite(im, overlay)


def main():
    if not SRC.exists():
        raise SystemExit(f"Missing {SRC}")

    if not CONV.exists():
        CONV.write_bytes(SRC.read_bytes())

    base = Image.open(CONV).convert("RGBA")
    w, h = base.size

    soot, ice, contrail = guess_regions(w, h)

    # Make it *obviously* different:
    out = base.copy()
    out = white_wash(out, soot, alpha=0.62)      # knock down soot dots
    out = white_wash(out, ice, alpha=0.55)       # knock down ice crystals
    out = draw_thinner_contrail(out, contrail)   # thinner contrail

    # Slight overall brightness bump so it reads as "cleaner"
    rgb = out.convert("RGB")
    rgb = ImageEnhance.Brightness(rgb).enhance(1.03)
    rgb = ImageEnhance.Contrast(rgb).enhance(0.98)

    rgb.save(LOW, format="PNG", optimize=True)
    print("Wrote:")
    print(" ", CONV)
    print(" ", LOW)
    print("Guessed regions (edit in script if needed):")
    print(" soot     ", soot)
    print(" ice      ", ice)
    print(" contrail ", contrail)


if __name__ == "__main__":
    main()
