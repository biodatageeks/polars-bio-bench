from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple


@dataclass
class Series:
    name: str
    values: List[Tuple[str, float]]  # (category, value)


def parse_benchmark_csv(csv_path: Path) -> List[Tuple[str, float]]:
    """Parse a benchmark CSV and return list of (Library, MeanSeconds).

    CSV expected header includes 'Library' and 'Mean (s)'.
    """
    values: List[Tuple[str, float]] = []
    with csv_path.open(newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            lib = row.get("Library")
            mean_s = row.get("Mean (s)")
            if lib is None or mean_s is None:
                # Try alternative column names if present
                # Fallback: try 'Mean' without units
                lib = row.get("Library", "?")
                mean_s = row.get("Mean")
            if mean_s is None:
                continue
            try:
                mean = float(str(mean_s).strip())
            except ValueError:
                # If it's like '0.33s' or contains units unintentionally, strip non-numeric
                cleaned = "".join(
                    ch for ch in str(mean_s) if (ch.isdigit() or ch in ".-")
                )
                if not cleaned:
                    continue
                mean = float(cleaned)
            values.append((str(lib), mean))
    return values


def infer_operation_and_pair(filename: str) -> Tuple[str, str] | None:
    """Infer (operation, pair) from filename like 'overlap-single-3tools_1-2.csv'."""
    name = filename.rsplit("/", 1)[-1]
    if not name.endswith(".csv"):
        return None
    stem = name[:-4]
    if "_" not in stem:
        return None
    left, pair = stem.rsplit("_", 1)
    # Operation is the portion before the first '-' (e.g., 'overlap')
    op = left.split("-", 1)[0]
    return op, pair


def layout_subplots(
    n: int, width: int, height: int, padding: int = 16
) -> List[Tuple[int, int, int, int]]:
    """Compute n horizontal subplots within an SVG canvas.

    Returns list of (x, y, w, h) for each subplot area.
    """
    if n <= 0:
        return []
    inner_w = width - padding * 2
    inner_h = height - padding * 2
    subplot_w = inner_w // n
    boxes: List[Tuple[int, int, int, int]] = []
    for i in range(n):
        x = padding + i * subplot_w
        y = padding
        boxes.append((x, y, subplot_w, inner_h))
    return boxes


def svg_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def draw_bar_subplot(
    op_name: str, data: List[Tuple[str, float]], x: int, y: int, w: int, h: int
) -> str:
    """Return SVG for a single bar subplot with title and value labels.

    - op_name: subplot title (operation)
    - data: list of (category, value)
    - (x, y, w, h): subplot bounding box
    """
    if not data:
        return f"""
        <g transform="translate({x},{y})">
          <rect x="0" y="0" width="{w}" height="{h}" fill="#fafafa" stroke="#ddd"/>
          <text x="{w/2:.1f}" y="{h/2:.1f}" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#999">No data</text>
        </g>
        """

    # Layout constants
    top_title_h = 24
    axis_bottom_h = 28
    left_pad = 12
    right_pad = 12
    plot_w = max(10, w - left_pad - right_pad)
    plot_h = max(10, h - top_title_h - axis_bottom_h)

    # Determine scaling
    max_val = max(v for _, v in data)
    if max_val <= 0:
        max_val = 1.0
    n = len(data)
    gap = 10
    bar_w = max(8, int((plot_w - gap * (n + 1)) / max(1, n)))

    # Colors matching parallel benchmark: GenomicRanges (blue), polars-bio (orange)
    color_map = {
        "genomicranges": "#1f77b4",  # Blue (matplotlib default)
        "polars_bio": "#ff7f0e",  # Orange (matplotlib default)
        "polars-bio": "#ff7f0e",  # Orange (alternative naming)
    }

    # Fallback colors for other libraries
    fallback_colors = [
        "#3b82f6",  # blue-500
        "#22c55e",  # green-500
        "#f59e0b",  # amber-500
        "#ef4444",  # red-500
        "#a855f7",  # purple-500
        "#06b6d4",  # cyan-500
    ]

    svg_parts: List[str] = []
    svg_parts.append(f'<g transform="translate({x},{y})">')
    svg_parts.append(
        f'<rect x="0" y="0" width="{w}" height="{h}" fill="#ffffff" stroke="#ddd"/>'
    )
    # Title
    svg_parts.append(
        f'<text x="{w/2:.1f}" y="{top_title_h - 6}" text-anchor="middle" font-family="sans-serif" font-size="14" font-weight="600">{svg_escape(op_name)}</text>'
    )

    # Bars
    origin_x = left_pad
    origin_y = top_title_h
    for i, (cat, val) in enumerate(data):
        h_norm = 0 if max_val == 0 else val / max_val
        bar_h = int(h_norm * (plot_h - 1))
        bx = origin_x + gap + i * (bar_w + gap)
        by = origin_y + (plot_h - bar_h)

        # Use color map for known libraries, fallback colors for others
        cat_lower = cat.lower()
        if cat_lower in color_map:
            color = color_map[cat_lower]
        else:
            color = fallback_colors[i % len(fallback_colors)]

        svg_parts.append(
            f'<rect x="{bx}" y="{by}" width="{bar_w}" height="{bar_h}" fill="{color}" />'
        )
        # Value label above the bar
        svg_parts.append(
            f'<text x="{bx + bar_w/2:.1f}" y="{by - 4}" text-anchor="middle" font-family="sans-serif" font-size="11" fill="#333">{val:.3f}s</text>'
        )
        # Category label
        svg_parts.append(
            f'<text x="{bx + bar_w/2:.1f}" y="{origin_y + plot_h + 16}" text-anchor="middle" font-family="sans-serif" font-size="11" fill="#333">{svg_escape(cat)}</text>'
        )

    # Simple y-axis max marker
    svg_parts.append(
        f'<text x="{left_pad}" y="{origin_y + 12}" text-anchor="start" font-family="sans-serif" font-size="10" fill="#777">max {max_val:.3f}s (lower is better)</text>'
    )

    svg_parts.append("</g>")
    return "\n".join(svg_parts)


def render_pair_figure(
    pair: str, op_to_data: Dict[str, List[Tuple[str, float]]], out_path: Path
) -> None:
    ops = ["overlap", "nearest", "count_overlaps"]
    n = len(ops)
    # Canvas size: width per subplot 360, height 280
    subplot_w = 360
    subplot_h = 280
    total_w = subplot_w * n + 32
    total_h = subplot_h + 32

    boxes = layout_subplots(n, total_w, total_h, padding=16)

    svg_parts: List[str] = []
    svg_parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{total_w}" height="{total_h}" viewBox="0 0 {total_w} {total_h}">'
    )
    # Global title
    svg_parts.append(
        f'<text x="{total_w/2:.1f}" y="18" text-anchor="middle" font-family="sans-serif" font-size="16" font-weight="600">Pair {svg_escape(pair)} — Mean runtime (s)</text>'
    )
    for (x, y, w, h), op in zip(boxes, ops):
        data = op_to_data.get(op, [])
        svg_parts.append(draw_bar_subplot(op, data, x, y + 8, w, h - 8))
    svg_parts.append("</svg>")

    out_path.write_text("\n".join(svg_parts))


def collect_results(results_dir: Path) -> Dict[str, Dict[str, List[Tuple[str, float]]]]:
    """Collect data grouped by pair then by operation.

    Returns mapping: pair -> { operation -> [(library, mean_s), ...] }
    """
    pair_to_ops: Dict[str, Dict[str, List[Tuple[str, float]]]] = {}
    for csv_path in results_dir.glob("*.csv"):
        inferred = infer_operation_and_pair(csv_path.name)
        if inferred is None:
            continue
        op, pair = inferred
        values = parse_benchmark_csv(csv_path)
        if not values:
            continue
        pair_to_ops.setdefault(pair, {})[op] = values
    return pair_to_ops


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate per-pair bar charts (SVG) from benchmark CSVs."
    )
    parser.add_argument(
        "--results-dir",
        type=Path,
        required=True,
        help="Directory containing benchmark CSVs (e.g., results/benchmark-2025-3tools-single-3ops)",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=None,
        help="Output directory for figures (defaults to <results-dir>/figures)",
    )
    args = parser.parse_args()

    results_dir: Path = args.results_dir
    out_dir: Path = args.out_dir or (results_dir / "figures")
    out_dir.mkdir(parents=True, exist_ok=True)

    pair_to_ops = collect_results(results_dir)
    if not pair_to_ops:
        print(f"No CSV data found in {results_dir}")
        return

    for pair, op_to_data in sorted(pair_to_ops.items()):
        out_path = out_dir / f"pair_{pair}.svg"
        render_pair_figure(pair, op_to_data, out_path)
        print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
