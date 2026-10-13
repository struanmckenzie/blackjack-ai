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

import os


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

    input_directory = "imperfect_maze"
    output_directory = "imperfect_maze_png"

    os.makedirs(output_directory, exist_ok=True)
    
    image_paths = [os.path.join(input_directory, filename) for filename in os.listdir(input_directory) if filename.endswith('.txt')]

    for file in image_paths:
        output_path = os.path.join(output_directory,os.path.splitext(os.path.basename(file))[0] + ".png")
        rows = read_grid(file)
        h, w = len(rows), len(rows[0])

        black_value, white_value = (1, 0)
        img = Image.new("L", (w, h), 255)
        img.putdata([0 if v == black_value else 255 for row in rows for v in row])

        img.save(output_path)
        print(f"Saved {file} ({img.width}x{img.height})")


if __name__ == "__main__":
    main()