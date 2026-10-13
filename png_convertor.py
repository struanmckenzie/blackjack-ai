#!/usr/bin/env python3
"""Convert a text file of 1s and 0s into a PNG, one pixel per value.

By default 0 -> white and 1 -> black.

Usage:
    python txt_to_png.py grid.txt                 # writes grid.png
    python txt_to_png.py grid.txt -o out.png
    python txt_to_png.py grid.txt --invert        # 1 -> white, 0 -> black
    python txt_to_png.py grid.txt --scale 10      # each value becomes a 10x10 block

Input can be space separated ("1 0 1") or unseparated ("101"), one row per line.

Requires Pillow:  pip install pillow
"""
import argparse
import sys
from pathlib import Path

from PIL import Image


def read_grid(path):
    rows = []
    with open(path) as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            tokens = line.split() if " " in line or "\t" in line or "," in line else list(line)
            tokens = [t for part in tokens for t in part.split(",") if t]
            if any(t not in ("0", "1") for t in tokens):
                sys.exit(f"Line {lineno}: only 0 and 1 are allowed.")
            rows.append([int(t) for t in tokens])
    if not rows:
        sys.exit("The file contains no data.")
    widths = {len(r) for r in rows}
    if len(widths) != 1:
        sys.exit(f"Rows have different lengths: {sorted(widths)}")
    return rows


def main():
    p = argparse.ArgumentParser(description="Turn a txt file of 1s and 0s into a PNG.")
    p.add_argument("input", help="path to the .txt file")
    p.add_argument("-o", "--output", help="output PNG path (default: input name with .png)")
    p.add_argument("--invert", action="store_true", help="1 = white, 0 = black")
    p.add_argument("--scale", type=int, default=1, help="pixels per value (default 1)")
    args = p.parse_args()

    rows = read_grid(args.input)
    h, w = len(rows), len(rows[0])

    black_value, white_value = (1, 0) if not args.invert else (0, 1)
    img = Image.new("L", (w, h), 255)
    img.putdata([0 if v == black_value else 255 for row in rows for v in row])

    if args.scale > 1:
        img = img.resize((w * args.scale, h * args.scale), Image.NEAREST)

    out = args.output or str(Path(args.input).with_suffix(".png"))
    img.save(out)
    print(f"Saved {out} ({img.width}x{img.height})")


if __name__ == "__main__":
    main()