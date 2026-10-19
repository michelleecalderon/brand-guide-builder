#!/usr/bin/env python3
"""WCAG 2.x contrast ratios for every ordered text-on-background pair in a palette.

Usage:
    python3 contrast_check.py '[{"name":"Pine","hex":"#2F5D50"},{"name":"Flour","hex":"#FAF7F0"}]'
    python3 contrast_check.py --file palette.json
    python3 contrast_check.py --file palette.json --json

Input is a JSON array of {"name": str, "hex": str}; hex may be 3 or 6 digits,
with or without "#". Output is a table sorted by ratio (highest first) with
AA / AAA pass marks for normal text (4.5:1 / 7:1), plus a count of
AA-passing pairs. The brand-guide flow needs at least 2 before the Colors
step is complete; the script exits with status 2 if that isn't met, so
callers can branch on it. Requires Python 3.8+, standard library only.
"""

import argparse
import json
import sys
from typing import Dict, List, Tuple

AA_NORMAL, AAA_NORMAL, AA_LARGE, AAA_LARGE = 4.5, 7.0, 3.0, 4.5
MIN_AA_PAIRS = 2


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    h = hex_color.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) != 6:
        raise ValueError(f"Invalid hex color: {hex_color!r}")
    try:
        return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    except ValueError:
        raise ValueError(f"Invalid hex color: {hex_color!r}") from None


def _linear(channel: int) -> float:
    c = channel / 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def relative_luminance(hex_color: str) -> float:
    r, g, b = (_linear(c) for c in hex_to_rgb(hex_color))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(hex_a: str, hex_b: str) -> float:
    la, lb = relative_luminance(hex_a), relative_luminance(hex_b)
    lighter, darker = max(la, lb), min(la, lb)
    return (lighter + 0.05) / (darker + 0.05)


def compute_pairs(palette: List[Dict[str, str]]) -> List[Dict]:
    """Every ordered pair (text on background) with ratio and pass flags."""
    names = [c["name"] for c in palette]
    if len(set(names)) != len(names):
        raise ValueError("Color names must be unique.")
    rows = []
    for fg in palette:
        for bg in palette:
            if fg["name"] == bg["name"]:
                continue
            ratio = contrast_ratio(fg["hex"], bg["hex"])
            rows.append({
                "pair": f"{fg['name']} on {bg['name']}",
                "text": fg["name"],
                "background": bg["name"],
                "ratio": round(ratio, 2),
                "aa": ratio >= AA_NORMAL,
                "aaa": ratio >= AAA_NORMAL,
                "aa_large": ratio >= AA_LARGE,
                "aaa_large": ratio >= AAA_LARGE,
            })
    return sorted(rows, key=lambda r: r["ratio"], reverse=True)


def format_table(rows: List[Dict]) -> str:
    width = max(len(r["pair"]) for r in rows) + 2
    lines = [f"{'COMBINATION':<{width}}{'RATIO':<8}{'AA':<5}{'AAA':<5}"]
    for r in rows:
        lines.append(
            f"{r['pair']:<{width}}{r['ratio']:<8}"
            f"{'yes' if r['aa'] else '-':<5}{'yes' if r['aaa'] else '-':<5}"
        )
    passing = sum(r["aa"] for r in rows)
    lines.append(f"\n{passing} of {len(rows)} combinations pass AA (4.5:1) for normal text.")
    if passing < MIN_AA_PAIRS:
        lines.append(
            f"Fewer than {MIN_AA_PAIRS} AA-passing combinations: adjust a tint/shade and re-run."
        )
    return "\n".join(lines)


def load_palette(args: argparse.Namespace) -> List[Dict[str, str]]:
    raw = open(args.file).read() if args.file else args.palette
    palette = json.loads(raw)
    if not isinstance(palette, list) or len(palette) < 2:
        raise ValueError("Palette must be a JSON array of at least 2 colors.")
    for c in palette:
        if "name" not in c or "hex" not in c:
            raise ValueError('Each color needs "name" and "hex".')
    return palette


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("palette", nargs="?", help="JSON array of {name, hex}")
    ap.add_argument("--file", help="Read the palette from a JSON file")
    ap.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = ap.parse_args(argv)
    if not args.palette and not args.file:
        ap.error("provide a palette JSON string or --file")
    try:
        rows = compute_pairs(load_palette(args))
    except (ValueError, json.JSONDecodeError, OSError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    passing = sum(r["aa"] for r in rows)
    print(json.dumps({"pairs": rows, "aa_passing": passing}, indent=2)
          if args.json else format_table(rows))
    return 0 if passing >= MIN_AA_PAIRS else 2


if __name__ == "__main__":
    sys.exit(main())
