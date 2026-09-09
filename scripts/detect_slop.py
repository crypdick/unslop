#!/usr/bin/env python3
"""Detect probable AI writing patterns ("slop") in text files.

Usage:
    python detect_slop.py FILE_OR_DIR [FILE_OR_DIR ...]
    python detect_slop.py --json report.json src/
    python detect_slop.py --threshold 3.0 draft.md

Exit codes:
    0  No slop detected above threshold
    1  Slop detected
    2  Usage error
"""

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

from slop_reports import print_report, print_summary
from slop_scanner import FileReport, Finding, scan_text, tokenize_lower

__all__ = ["FileReport", "Finding", "collect_files", "scan_text", "tokenize_lower"]

TEXT_EXTENSIONS = {
    ".txt",
    ".md",
    ".mdx",
    ".rst",
    ".tex",
    ".adoc",
    ".html",
    ".htm",
    ".xml",
    ".py",
    ".js",
    ".ts",
    ".jsx",
    ".tsx",
    ".rb",
    ".go",
    ".rs",
    ".java",
    ".css",
    ".scss",
    ".yaml",
    ".yml",
    ".toml",
    ".json",
    ".sh",
    ".bash",
    ".zsh",
    ".csv",
}

# Directories to always skip
SKIP_DIRS = {
    ".git",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "dist",
    "build",
    ".next",
    ".cache",
    "vendor",
}


def collect_files(paths: list[str], extensions: set[str] | None = None) -> list[Path]:
    """Collect text files from the given paths (files or directories)."""
    exts = extensions or TEXT_EXTENSIONS
    result = []
    for p in paths:
        path = Path(p)
        if path.is_file():
            result.append(path)
        elif path.is_dir():
            result.extend(
                child
                for child in sorted(path.rglob("*"))
                if child.is_file()
                and child.suffix in exts
                and not any(skip in child.parts for skip in SKIP_DIRS)
            )
        else:
            print(f"warning: {p} is not a file or directory, skipping", file=sys.stderr)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Detect probable AI writing patterns (slop) in text files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
        "  %(prog)s draft.md\n"
        "  %(prog)s --verbose src/\n"
        "  %(prog)s --json report.json docs/\n"
        "  %(prog)s --threshold 5.0 blog-posts/\n"
        "  echo 'some text' | %(prog)s -\n",
    )
    parser.add_argument("paths", nargs="*", default=["-"], help="files or directories to scan (- for stdin)")
    parser.add_argument("--json", metavar="FILE", help="write JSON report to FILE")
    parser.add_argument(
        "--threshold", type=float, default=0.0, help="minimum slop score to report a file (default: 0)"
    )
    parser.add_argument("--no-color", action="store_true", help="disable colored output")
    parser.add_argument("--verbose", "-v", action="store_true", help="show low-severity findings too")
    args = parser.parse_args()

    use_color = not args.no_color and sys.stdout.isatty()

    # Handle stdin
    if args.paths == ["-"]:
        text = sys.stdin.read()
        reports = [scan_text(text, "<stdin>")]
    else:
        files = collect_files(args.paths)
        if not files:
            print("No text files found.", file=sys.stderr)
            sys.exit(2)

        reports = []
        for fpath in files:
            try:
                text = fpath.read_text(encoding="utf-8", errors="replace")
                reports.append(scan_text(text, str(fpath)))
            except (OSError, UnicodeDecodeError) as e:
                print(f"warning: skipping {fpath}: {e}", file=sys.stderr)

    # Filter by threshold
    for r in reports:
        if r.slop_score >= args.threshold:
            print_report(r, use_color=use_color, verbose=args.verbose)

    print_summary(reports)

    # JSON output
    if args.json:
        json_data = []
        for r in reports:
            d = {
                "path": r.path,
                "word_count": r.word_count,
                "ai_vocab_count": r.ai_vocab_count,
                "ai_vocab_density": round(r.ai_vocab_density, 2),
                "slop_score": round(r.slop_score, 2),
                "findings": [asdict(f) for f in r.findings],
            }
            json_data.append(d)
        Path(args.json).write_text(json.dumps(json_data, indent=2))
        print(f"\nJSON report written to {args.json}")

    # Exit code: 1 if any slop found above threshold
    has_slop = any(r.slop_score > args.threshold for r in reports)
    sys.exit(1 if has_slop else 0)


if __name__ == "__main__":
    main()
