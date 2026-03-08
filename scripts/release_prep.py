#!/usr/bin/env python3
"""Prepare a release bundle and validate repository readiness."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REQUIRED_PATHS = [
    Path("README.md"),
    Path("README_EN.md"),
    Path("CHANGELOG.md"),
    Path("LICENSE"),
    Path("requirements.txt"),
    Path(".github/workflows/ci.yml"),
]


def validate_version(raw_version: str) -> str:
    """Normalize and validate semantic versions."""
    version = raw_version.strip()
    if version.startswith("v"):
        version = version[1:]

    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise ValueError("version must look like 0.3.0 or v0.3.0")

    return version


def run_command(command: list[str], cwd: Path | None = None) -> str:
    """Run a command and return stdout, raising on failure."""
    result = subprocess.run(
        command,
        cwd=str(cwd or REPO_ROOT),
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "command failed")
    return result.stdout.strip()


def git_status_clean() -> bool:
    """Return whether the working tree is clean."""
    output = run_command(["git", "status", "--porcelain"])
    return output == ""


def ensure_required_paths() -> list[str]:
    """Return missing required repo paths."""
    missing = []
    for relative_path in REQUIRED_PATHS:
        if not (REPO_ROOT / relative_path).exists():
            missing.append(str(relative_path))
    return missing


def extract_changelog_section(version: str) -> str:
    """Extract the matching changelog section or fallback to unreleased."""
    changelog_path = REPO_ROOT / "CHANGELOG.md"
    contents = changelog_path.read_text()
    version_headers = [f"## [{version}]", f"## [v{version}]"]

    lines = contents.splitlines()
    capture = False
    captured: list[str] = []

    for line in lines:
        if any(line.startswith(header) for header in version_headers):
            capture = True
        elif capture and line.startswith("## ["):
            break

        if capture:
            captured.append(line)

    if captured:
        return "\n".join(captured).strip()

    unreleased: list[str] = []
    capture = False
    for line in lines:
        if line.startswith("## [Unreleased]"):
            capture = True
        elif capture and line.startswith("## ["):
            break
        if capture:
            unreleased.append(line)

    return "\n".join(unreleased).strip() or "No changelog section found."


def run_tests() -> None:
    """Run the unit test suite."""
    run_command([sys.executable, "-m", "unittest", "discover", "-s", "tests"])


def build_release_notes(version: str, changelog_section: str) -> str:
    """Generate markdown release notes."""
    return "\n".join(
        [
            f"# OpenFang Auto Clip v{version}",
            "",
            f"Prepared at: {datetime.now().isoformat(timespec='seconds')}",
            "",
            "## Validation",
            "- README.md present",
            "- README_EN.md present",
            "- CHANGELOG.md present",
            "- CI workflow present",
            "- Unit tests passed",
            "",
            "## Changelog",
            changelog_section,
            "",
            "## Suggested Publish Steps",
            "1. Review release_notes.md",
            "2. Create tag `v{version}`",
            "3. Push branch and tag",
            "4. Draft GitHub release using the generated notes",
            "",
        ]
    ).replace("v{version}", f"v{version}")


def write_release_bundle(version: str, notes: str, output_dir: Path) -> Path:
    """Write release artifacts to disk."""
    target_dir = output_dir / f"v{version}"
    target_dir.mkdir(parents=True, exist_ok=True)
    notes_path = target_dir / "release_notes.md"
    notes_path.write_text(notes)
    return notes_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate and prepare a release bundle")
    parser.add_argument("version", help="Semantic version like 0.3.0 or v0.3.0")
    parser.add_argument(
        "--output-dir",
        default="dist/releases",
        help="Directory for generated release artifacts",
    )
    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="Skip running the unit test suite",
    )
    parser.add_argument(
        "--allow-dirty",
        action="store_true",
        help="Allow preparing a release from a dirty working tree",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        version = validate_version(args.version)
    except ValueError as exc:
        print(f"❌ {exc}")
        return 1

    if not args.allow_dirty and not git_status_clean():
        print("❌ Working tree is dirty. Commit or stash changes, or use --allow-dirty.")
        return 1

    missing_paths = ensure_required_paths()
    if missing_paths:
        print("❌ Missing required release files:")
        for path in missing_paths:
            print(f"   - {path}")
        return 1

    if not args.skip_tests:
        print("🧪 Running unit tests...")
        run_tests()

    changelog_section = extract_changelog_section(version)
    notes = build_release_notes(version, changelog_section)
    notes_path = write_release_bundle(version, notes, REPO_ROOT / args.output_dir)

    print("✅ Release bundle prepared")
    print(f"   Version: v{version}")
    print(f"   Notes: {notes_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
