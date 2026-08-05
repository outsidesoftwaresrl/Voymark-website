#!/usr/bin/env python3
"""Render /favicon.ico at the site root.

    python3 scripts/make_favicon.py

**Why a root .ico when the pages already link a favicon.** Every page carries
`<link rel="icon" href=".../favicon-32.png">`, and that covers browsers
rendering our HTML. It does not cover everything else: browsers request
`/favicon.ico` from the origin root regardless of link tags, and so do RSS
readers, link unfurlers, bookmark managers, and anything showing the site
without parsing its head. On GitHub Pages a missing one is a 404 per visit.

**Why redrawn rather than rasterised from `assets/img/favicon.svg`.** There is
no cairosvg or rsvg here, and it is the better result anyway: each size is
drawn at its own scale rather than downsampled from 64px, which is the
difference between a legible 16px mark and a burgundy smudge. The geometry
below mirrors the SVG exactly — same radii, same stroke widths, same colours —
so the two cannot drift without someone editing both.

**Root, not `assets/img/`.** `/favicon.ico` is the whole point; a copy under
`assets/` would never be requested by the clients this exists for. It serves
correctly from `voymark.app/favicon.ico`. Under the GitHub Pages project URL
the origin root is `outsidesoftwaresrl.github.io`, which is not ours — that is
unavoidable and does not matter, since the apex domain is the canonical one.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PAPER = (246, 241, 230)      # --paper, assets/style.css:39
BURGUNDY = (122, 35, 51)     # #7A2333, the seal colour in favicon.svg
SIZES = [16, 32, 48, 64]

SERIF_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSerif.ttf",
]


def serif(size: int) -> ImageFont.FreeTypeFont:
    for path in SERIF_CANDIDATES:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    raise SystemExit("no serif font found — apt-get install fonts-dejavu-core")


def draw(size: int) -> Image.Image:
    """The seal at one size, simplified when the size demands it.

    A favicon is not a logo shrunk down. At 16px the SVG's inner hairline ring
    is 0.27 of a pixel wide: it renders as a grey haze that only lowers the
    contrast of everything around it, and the outer ring at 0.8px is barely
    there either. So below 24px the mark becomes one heavier ring and a bolder
    V — recognisably the same seal, legible at the size it is actually used.
    Above that, the geometry is the SVG's exactly.
    """
    small = size < 24
    # 8x supersample then downscale: PIL's ImageDraw has no antialiasing, and
    # thin concentric circles are exactly where that shows.
    s = size * 8
    img = Image.new("RGB", (s, s), PAPER)
    d = ImageDraw.Draw(img)
    c = s / 2

    # Proportions from favicon.svg, on its 64-unit viewBox.
    rings = ((25, 5.0),) if small else ((24, 3.2), (18.5, 1.1))
    for radius, width in rings:
        r = s * radius / 64
        d.ellipse([c - r, c - r, c + r, c + r],
                  outline=BURGUNDY, width=max(1, round(s * width / 64)))

    font = serif(round(s * (30 if small else 34) / 64))
    box = d.textbbox((0, 0), "V", font=font)
    x = c - (box[2] - box[0]) / 2 - box[0]
    y = c - (box[3] - box[1]) / 2 - box[1]
    d.text((x, y), "V", font=font, fill=BURGUNDY)
    if small:
        # Fake a bolder weight by overprinting: a serif V at 15 effective
        # pixels is otherwise one hairline stroke and one thick one.
        for dx, dy in ((s / 64, 0), (0, s / 64), (s / 64, s / 64)):
            d.text((x + dx, y + dy), "V", font=font, fill=BURGUNDY)
    return img.resize((size, size), Image.LANCZOS)


def main() -> int:
    if not Path("assets/img/favicon.svg").exists():
        print("run this from the website repo root")
        return 1

    images = [draw(n) for n in SIZES]
    # Largest first: PIL's ICO writer skips any requested size larger than the
    # base image, and matches the rest against append_images by exact size —
    # so every frame here is the one drawn at that size, not a downscale.
    images[-1].save("favicon.ico", format="ICO",
                    sizes=[(n, n) for n in SIZES], append_images=images[:-1])

    written = sorted(Image.open("favicon.ico").info.get("sizes", []))
    print(f"favicon.ico — {len(written)} frames: "
          f"{', '.join(f'{w}x{h}' for w, h in written)} "
          f"({Path('favicon.ico').stat().st_size} bytes)")
    if len(written) != len(SIZES):
        print("expected one frame per size")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
