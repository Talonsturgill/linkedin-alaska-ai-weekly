"""Hard technical gate for a rendered Alaska.Ai artwork.

Usage:
    python .claude/skills/alaska-ai-artwork/qa_check.py \
        --image out/post_image.png --date "26 JUN 2026" --column "THE STACK"

Checks are TECHNICAL only (dimensions, blankness, palette count, meta
completeness, date consistency). Aesthetic judgement happens in the
skill's eval loop — the model looks at the image; this script only stops
mechanically broken output from shipping. Exit 0 = pass, 1 = fail with
reasons on stdout.
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

REQUIRED_META = [
    "date", "column", "kicker", "headline", "style_family", "palette",
    "hue_family", "composition", "motifs", "technique_stack", "seed",
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", required=True)
    ap.add_argument("--date", required=True,
                    help='caption date the art must carry, e.g. "26 JUN 2026"')
    ap.add_argument("--column", required=True,
                    help='column kicker, e.g. "THE STACK"')
    args = ap.parse_args()

    errors = []
    p = Path(args.image)

    if not p.exists():
        print(f"FAIL: {p} does not exist")
        sys.exit(1)

    img = Image.open(p)
    if img.format != "PNG":
        errors.append(f"format is {img.format}, expected PNG")
    if img.size != (1080, 1080):
        errors.append(f"dimensions {img.size}, expected (1080, 1080)")

    kb = p.stat().st_size / 1024
    if not (60 <= kb <= 2500):
        errors.append(f"file size {kb:.0f} KB outside sane range 60-2500 KB")

    arr = np.asarray(img.convert("RGB"), float)
    if arr.std() < 12:
        errors.append(f"pixel stddev {arr.std():.1f} < 12 — image is "
                      "blank or near-flat")
    small = np.asarray(img.convert("RGB").resize((128, 128)))
    uniq = len(np.unique(small.reshape(-1, 3), axis=0))
    if uniq < 40:
        errors.append(f"only {uniq} distinct colors at 128px — render "
                      "likely failed or degenerate")

    meta_path = Path(str(p) + ".meta.json")
    if not meta_path.exists():
        errors.append("meta sidecar missing")
    else:
        try:
            meta = json.loads(meta_path.read_text())
        except Exception as e:
            errors.append(f"meta sidecar unreadable: {e}")
            meta = {}
        for k in REQUIRED_META:
            if k not in meta or meta[k] in (None, "", []):
                errors.append(f"meta missing required key: {k}")
        if meta.get("date") != args.date:
            errors.append(f'meta date "{meta.get("date")}" != expected '
                          f'"{args.date}" — date-consistency gate')
        if meta.get("kicker") != args.column:
            errors.append(f'meta kicker "{meta.get("kicker")}" != expected '
                          f'"{args.column}"')
        if isinstance(meta.get("palette"), list) and \
                not (2 <= len(meta["palette"]) <= 7):
            errors.append(f'palette has {len(meta["palette"])} inks; '
                          "expected 2-7 (limited-palette discipline)")

    if errors:
        print("FAIL:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print(f"PASS: {p} 1080x1080 PNG, {kb:.0f} KB, stddev {arr.std():.0f}, "
          f"{uniq} colors@128, meta complete, date + kicker consistent")


if __name__ == "__main__":
    main()
