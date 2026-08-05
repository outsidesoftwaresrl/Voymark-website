#!/usr/bin/env python3
"""Derive the site's screenshot set from the iOS repo's captures.

The site shows eight of the eighteen App Store captures, downscaled and
converted to WebP. That conversion used to be done by hand, which is why the
site was still serving the 2026-08-01 set on 2026-08-05 — the app repo
re-captured all eighteen on `1.0.240` and nothing carried them across, because
nothing was written down to carry them.

Usage, from the website repo root:

    python3 scripts/make_site_shots.py ../Voymark/docs/screenshots/iphone-6.9

Then run `python3 scripts/build_i18n.py` — the pages reference these by
filename, so they do not change, but regenerating keeps the two in step.

**Why 720x1564.** They render in a 360px slot, so this is exactly 2x for
retina and nothing more. WebP at quality 82 puts the eight at ~350 KB where
the source PNGs are 8.7 MB; PNG at this size would still be about 2 MB.
WebP has shipped in every browser since Safari 14 (2020), the same vintage as
the `prefers-color-scheme` and WOFF2 this site already depends on.

**RGBA is flattened onto the page cream**, not onto white. The captures carry
an alpha channel they do not use, and PIL's WebP encoder keeps it — which
costs bytes for nothing and, if a shot ever did have a transparent corner,
would show the browser's backdrop instead of the site's.
"""
import sys
from pathlib import Path

from PIL import Image

# Source file → site filename. Only these eight are used; the other ten
# captures exist for App Store Connect, which needs a different set.
MAPPING = {
    "01-passport.png": "shot-passport.webp",
    "02-map-atlas-world.png": "shot-map.webp",
    "05-map-paper.png": "shot-paper.webp",
    "06-time-machine.png": "shot-time-machine.webp",
    "07-timeline.png": "shot-timeline.webp",
    "08-trip-detail.png": "shot-trip.webp",
    "09-photo-import.png": "shot-photo-import.webp",
    "15-statistics.png": "shot-stats.webp",
}

TARGET = (720, 1564)
QUALITY = 82
PAPER = (246, 241, 230)  # --paper, assets/style.css:39


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    src = Path(sys.argv[1])
    if not src.is_dir():
        print(f"not a directory: {src}")
        return 1

    out = Path("assets/img")
    if not out.is_dir():
        print("run this from the website repo root")
        return 1

    total = 0
    for source_name, site_name in MAPPING.items():
        source = src / source_name
        if not source.exists():
            print(f"MISSING {source} — aborting rather than leaving a mixed set")
            return 1

        image = Image.open(source)
        if image.mode == "RGBA":
            flat = Image.new("RGB", image.size, PAPER)
            flat.paste(image, mask=image.split()[3])
            image = flat
        else:
            image = image.convert("RGB")

        # LANCZOS: these are 1320px screenshots of text-heavy UI going to
        # 720px. Anything cheaper visibly softens the MRZ strip and the
        # statistics figures, which are the details the shots exist to show.
        image = image.resize(TARGET, Image.LANCZOS)
        target = out / site_name
        image.save(target, "WEBP", quality=QUALITY, method=6)
        size = target.stat().st_size
        total += size
        print(f"{source_name:32} -> {site_name:26} {size // 1024:4d} KB")

    print(f"{'':32}    {'total':26} {total // 1024:4d} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
