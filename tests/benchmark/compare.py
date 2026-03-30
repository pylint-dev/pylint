# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Compare two pytest-benchmark JSON results and output a markdown summary."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_benchmarks(path: Path) -> dict[str, dict[str, Any]]:
    """Load benchmark results from a pytest-benchmark JSON file."""
    data = json.loads(path.read_text())
    return {b["name"]: b["stats"] for b in data["benchmarks"]}


def format_time(seconds: float) -> str:
    """Format seconds into a human-readable string."""
    if seconds >= 1:
        return f"{seconds:.3f}s"
    if seconds >= 0.001:
        return f"{seconds * 1000:.1f}ms"
    return f"{seconds * 1_000_000:.0f}µs"


def compare(base_path: Path, pr_path: Path, threshold: float = 5.0) -> str:
    """Compare two benchmark results and return a markdown table.

    Args:
        base_path: Path to the base (main) benchmark JSON.
        pr_path: Path to the PR benchmark JSON.
        threshold: Percentage change above which to flag a result.

    Returns:
        Markdown-formatted comparison string.
    """
    base = load_benchmarks(base_path)
    pr = load_benchmarks(pr_path)

    all_names = sorted(set(base) | set(pr))
    if not all_names:
        return "No benchmarks found."

    rows: list[tuple[str, str, str, str, str]] = []
    has_significant = False

    for name in all_names:
        if name not in base or name not in pr:
            continue
        base_median = base[name]["median"]
        pr_median = pr[name]["median"]
        delta_pct = (pr_median - base_median) / base_median * 100

        if abs(delta_pct) >= threshold:
            has_significant = True
            if delta_pct > 0:
                flag = "🔴"
            else:
                flag = "🟢"
        else:
            flag = ""

        # Shorten test name for readability
        short_name = name.split("::")[-1]

        rows.append(
            (
                short_name,
                format_time(base_median),
                format_time(pr_median),
                f"{delta_pct:+.1f}%",
                flag,
            )
        )

    lines = []
    lines.append("## Benchmark comparison")
    lines.append("")
    lines.append(f"Threshold: ±{threshold:.0f}%")
    lines.append("")
    lines.append("| Benchmark | main | PR | Change | |")
    lines.append("|:----------|-----:|---:|-------:|-|")
    for name, base_t, pr_t, delta, flag in rows:
        lines.append(f"| `{name}` | {base_t} | {pr_t} | {delta} | {flag} |")

    if not has_significant:
        lines.append("")
        lines.append("No significant performance changes detected.")

    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base", required=True, type=Path, help="Base (main) benchmark JSON"
    )
    parser.add_argument("--pr", required=True, type=Path, help="PR benchmark JSON")
    parser.add_argument(
        "--threshold", type=float, default=5.0, help="Significance threshold (%%)"
    )
    parser.add_argument("--output", type=Path, help="Output file (default: stdout)")
    args = parser.parse_args()

    result = compare(args.base, args.pr, args.threshold)

    if args.output:
        args.output.write_text(result)
    else:
        print(result)


if __name__ == "__main__":
    main()
