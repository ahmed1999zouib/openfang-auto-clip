#!/usr/bin/env python3
"""Generate a launch kit from a benchmark report."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REPORT = REPO_ROOT / "examples" / "benchmark" / "sample_benchmark_report.json"


def load_report(report_path: Path) -> dict:
    """Load a benchmark report from disk."""
    with report_path.open() as handle:
        return json.load(handle)


def build_launch_markdown(report: dict) -> str:
    """Build launch-ready markdown copy from the benchmark report."""
    benchmark = report["benchmark"]
    timings = report["timings"]
    artifacts = report["artifacts"]
    transform = report["transform_result"]

    return "\n".join(
        [
            "# OpenFang Auto Clip Launch Kit",
            "",
            "## Short Pitch",
            "OpenFang Auto Clip is a local-first pipeline for turning long videos into platform-ready short clips with reproducible transformation and operator-friendly outputs.",
            "",
            "## Proof Points",
            f"- Synthetic demo duration: {benchmark['duration_seconds']}s",
            f"- Transform level: {benchmark['transform_level']}",
            f"- Clips generated: {artifacts['clip_count']}",
            f"- Total benchmark runtime: {timings['total_seconds']}s",
            f"- Transformation status: {transform['status']}",
            "",
            "## Shareable Assets",
            f"- Storyboard: `{artifacts.get('storyboard_path')}`",
            f"- Preview frame: `{artifacts.get('preview_path')}`",
            f"- Benchmark report: `benchmark_report.json`",
            "",
            "## Suggested X / LinkedIn Post",
            "",
            "```text",
            "Open-sourced a local-first video repurposing pipeline:",
            "",
            "- reproducible benchmark demo",
            "- FFmpeg-based Level 1 transform",
            "- local web manager + task history",
            "- automated release workflow",
            "",
            f"Latest benchmark: {artifacts['clip_count']} clips in {timings['total_seconds']}s using synthetic media.",
            "",
            "Repo: https://github.com/outhsics/openfang-auto-clip",
            "```",
            "",
            "## Suggested Release Checklist",
            "- Attach the storyboard image to the release",
            "- Link to the benchmark README",
            "- Mention the exact benchmark runtime",
            "- Keep claims aligned with the current Reality Check table",
            "",
        ]
    )


def write_launch_kit(markdown: str, output_dir: Path) -> Path:
    """Write the launch kit markdown to disk."""
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "launch_post.md"
    output_path.write_text(markdown)
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a launch kit from a benchmark report")
    parser.add_argument(
        "--report",
        default=str(DEFAULT_REPORT),
        help="Path to a benchmark report JSON file",
    )
    parser.add_argument(
        "--output-dir",
        default="dist/launch-kit",
        help="Directory for generated launch materials",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = load_report(Path(args.report))
    markdown = build_launch_markdown(report)
    output_path = write_launch_kit(markdown, REPO_ROOT / args.output_dir)
    print("✅ Launch kit generated")
    print(f"   Report: {args.report}")
    print(f"   Output: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
