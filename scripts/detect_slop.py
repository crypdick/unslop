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
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path

# ---------------------------------------------------------------------------
# Pattern definitions
# ---------------------------------------------------------------------------

# Tier 1: Dead giveaways when clustered
AI_VOCABULARY = {
    # Classic LLM lexicon
    "delve", "tapestry", "pivotal", "crucial", "underscore", "vibrant",
    "meticulous", "intricate", "testament", "garner", "bolstered",
    "fostering", "showcasing", "highlighting", "emphasizing", "enduring",
    "nuanced", "multifaceted", "comprehensive", "robust", "leverage",
    "realm", "paradigm", "cornerstone", "beacon", "spearhead",
    "demystify", "unpack", "harness", "catalyze", "synergy", "holistic",
    "granular", "unravel",
    # Inflation words
    "groundbreaking", "revolutionary", "transformative", "game-changing",
    "unprecedented", "invaluable", "indispensable", "indelible",
}

# Words that are only AI-ish when used metaphorically (need context)
CONTEXT_DEPENDENT = {"landscape", "navigate", "deep dive", "enhance"}

# Formulaic phrases — regex patterns with display names
FORMULAIC_PHRASES = [
    # Significance inflation
    (r"\bis a testament to\b", "significance inflation: 'is a testament to'"),
    (r"\bstands as a\b", "copulative avoidance: 'stands as a'"),
    (r"\bserves as a\b", "copulative avoidance: 'serves as a'"),
    (r"\bplays a (?:vital|crucial|pivotal|key) role\b", "significance inflation: 'plays a [vital/crucial/pivotal] role'"),
    (r"\bunderscores the importance\b", "significance inflation: 'underscores the importance'"),
    (r"\breflects? broader\b", "significance inflation: 'reflects broader'"),
    (r"\bsetting the stage for\b", "significance inflation: 'setting the stage for'"),
    (r"\bkey turning point\b", "significance inflation: 'key turning point'"),
    (r"\bindelible mark\b", "significance inflation: 'indelible mark'"),
    (r"\bevolving landscape\b", "significance inflation: 'evolving landscape'"),
    (r"\bat the intersection of\b", "significance inflation: 'at the intersection of'"),
    (r"\bin today'?s (?:rapidly )?(?:evolving|changing|digital)\b", "formulaic opener: 'in today's rapidly evolving...'"),

    # "Not just X but Y"
    (r"\bnot just\b.{1,40}\bbut (?:also|a)\b", "'not just X, but also Y' construction"),
    (r"\bmore than just\b", "'more than just' construction"),
    (r"\bisn'?t merely\b", "'isn't merely' construction"),

    # Promotional
    (r"\bboasts a\b", "promotional: 'boasts a'"),
    (r"\brich tapestry\b", "promotional: 'rich tapestry'"),
    (r"\bnestled in the heart of\b", "promotional: 'nestled in the heart of'"),
    (r"\bdiverse array\b", "promotional: 'diverse array'"),
    (r"\bcommitment to (?:excellence|innovation|quality)\b", "promotional: 'commitment to excellence/innovation'"),

    # Vague attribution
    (r"\bexperts (?:argue|suggest|believe|note)\b", "vague attribution: 'experts argue/suggest'"),
    (r"\bindustry reports (?:suggest|indicate|show)\b", "vague attribution: 'industry reports suggest'"),
    (r"\bit is widely (?:recognized|known|accepted)\b", "vague attribution: 'it is widely recognized'"),
    (r"\bstudies have shown\b", "vague attribution: 'studies have shown'"),

    # Formulaic conclusions
    (r"\bdespite (?:its|these|the) .{1,30}(?:challenges|limitations)\b", "formulaic conclusion: 'despite its... challenges'"),
    (r"\bas \w+ continues? to evolve\b", "formulaic conclusion: 'as X continues to evolve'"),
    (r"\bmoving forward\b", "formulaic conclusion: 'moving forward'"),
    (r"\bonly time will tell\b", "formulaic conclusion: 'only time will tell'"),

    # Filler phrases
    (r"\bit'?s worth noting that\b", "filler: 'it's worth noting that'"),
    (r"\bit'?s important to (?:remember|note|recognize)\b", "filler: 'it's important to remember'"),
    (r"\bit goes without saying\b", "filler: 'it goes without saying'"),
    (r"\bat the end of the day\b", "filler: 'at the end of the day'"),
    (r"\bwhen it comes to\b", "filler: 'when it comes to'"),
    (r"\bthe reality is that\b", "filler: 'the reality is that'"),

    # Collaborative address
    (r"\blet'?s (?:delve|dive|unpack|explore|examine)\b", "collaborative address: 'let's delve/dive/explore'"),
    (r"\bas we'?ll see\b", "collaborative address: 'as we'll see'"),
    (r"\bhere'?s (?:the thing|why)\b", "collaborative address: 'here's the thing/why'"),
]

# Dangling present participle fillers (end-of-sentence)
DANGLING_PARTICIPLE_RE = re.compile(
    r",\s*(?:thereby\s+)?"
    r"(?:highlighting|underscoring|emphasizing|showcasing|reflecting|"
    r"demonstrating|illustrating|reinforcing|fostering|ensuring|"
    r"contributing to|paving the way for|signaling|solidifying)"
    r"\b[^.!?]*[.!?]",
    re.IGNORECASE,
)

# Compile formulaic patterns
COMPILED_PHRASES = [(re.compile(p, re.IGNORECASE), name) for p, name in FORMULAIC_PHRASES]

# Transition words that AI overuses at sentence starts
TRANSITION_STARTERS = re.compile(
    r"^(?:Additionally|Furthermore|Moreover|Importantly|Notably|"
    r"Interestingly|That said|Nevertheless|Consequently|Subsequently|"
    r"Ultimately|Essentially|Fundamentally)[,:]?\s",
    re.MULTILINE,
)

# Em dash (for density check)
EM_DASH_RE = re.compile(r"\u2014|--")


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

@dataclass
class Finding:
    line: int
    severity: str  # "high", "medium", "low"
    category: str
    message: str
    text: str  # the matched text snippet

    @property
    def severity_weight(self) -> float:
        return {"high": 3.0, "medium": 1.5, "low": 0.5}[self.severity]


@dataclass
class FileReport:
    path: str
    findings: list[Finding] = field(default_factory=list)
    word_count: int = 0
    ai_vocab_count: int = 0
    ai_vocab_density: float = 0.0
    slop_score: float = 0.0

    @property
    def has_slop(self) -> bool:
        return self.slop_score > 0


def tokenize_lower(text: str) -> list[str]:
    """Split text into lowercase word tokens."""
    return re.findall(r"[a-z]+(?:'[a-z]+)?", text.lower())


def scan_text(text: str, filepath: str = "<stdin>") -> FileReport:
    """Analyze text for AI writing patterns. Returns a FileReport."""
    report = FileReport(path=filepath)
    lines = text.split("\n")
    words = tokenize_lower(text)
    report.word_count = len(words)

    if report.word_count < 10:
        return report

    # --- Per-line and per-sentence analysis ---
    for line_num, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped:
            continue

        # Formulaic phrases
        for pattern, name in COMPILED_PHRASES:
            for match in pattern.finditer(stripped):
                report.findings.append(Finding(
                    line=line_num,
                    severity="high" if "significance" in name or "copulative" in name else "medium",
                    category="formulaic_phrase",
                    message=name,
                    text=match.group(0)[:80],
                ))

        # Dangling participle filler
        for match in DANGLING_PARTICIPLE_RE.finditer(stripped):
            report.findings.append(Finding(
                line=line_num,
                severity="medium",
                category="dangling_participle",
                message="dangling participle filler clause",
                text=match.group(0).strip()[:80],
            ))

        # AI vocabulary clustering (per-sentence)
        sentences = re.split(r"[.!?]+", stripped)
        for sentence in sentences:
            sent_words = tokenize_lower(sentence)
            ai_words_in_sent = [w for w in sent_words if w in AI_VOCABULARY]
            if len(ai_words_in_sent) >= 3:
                report.findings.append(Finding(
                    line=line_num,
                    severity="high",
                    category="vocab_cluster",
                    message=f"AI vocabulary cluster: {', '.join(ai_words_in_sent)}",
                    text=sentence.strip()[:80],
                ))
            elif len(ai_words_in_sent) == 2 and len(sent_words) < 20:
                report.findings.append(Finding(
                    line=line_num,
                    severity="low",
                    category="vocab_cluster",
                    message=f"AI vocabulary pair in short sentence: {', '.join(ai_words_in_sent)}",
                    text=sentence.strip()[:80],
                ))

        # Transition word starters
        if TRANSITION_STARTERS.match(stripped):
            report.findings.append(Finding(
                line=line_num,
                severity="low",
                category="transition_starter",
                message="sentence starts with overused transition word",
                text=stripped[:60],
            ))

    # --- Document-level analysis ---

    # AI vocabulary density
    ai_words = [w for w in words if w in AI_VOCABULARY]
    report.ai_vocab_count = len(ai_words)
    report.ai_vocab_density = (len(ai_words) / len(words)) * 100 if words else 0

    if report.ai_vocab_density > 1.5:
        report.findings.append(Finding(
            line=0,
            severity="high",
            category="vocab_density",
            message=f"high AI vocabulary density: {report.ai_vocab_density:.1f}% ({len(ai_words)} words in {len(words)})",
            text=", ".join(sorted(set(ai_words))),
        ))
    elif report.ai_vocab_density > 0.5:
        report.findings.append(Finding(
            line=0,
            severity="medium",
            category="vocab_density",
            message=f"elevated AI vocabulary density: {report.ai_vocab_density:.1f}%",
            text=", ".join(sorted(set(ai_words))),
        ))

    # Em dash density
    em_dashes = len(EM_DASH_RE.findall(text))
    em_dash_rate = em_dashes / (len(words) / 100) if words else 0
    if em_dash_rate > 0.5:
        report.findings.append(Finding(
            line=0,
            severity="low",
            category="em_dash_density",
            message=f"em dash density: {em_dashes} em dashes per {len(words)} words ({em_dash_rate:.1f}/100 words)",
            text="",
        ))

    # Transition word density
    transition_count = len(TRANSITION_STARTERS.findall(text))
    para_count = len([p for p in text.split("\n\n") if p.strip()])
    if para_count > 2 and transition_count / para_count > 0.25:
        report.findings.append(Finding(
            line=0,
            severity="medium",
            category="transition_density",
            message=f"high transition word density: {transition_count}/{para_count} paragraphs start with transition words",
            text="",
        ))

    # Compute overall slop score (weighted findings per 100 words)
    raw_score = sum(f.severity_weight for f in report.findings)
    report.slop_score = (raw_score / len(words)) * 100 if words else 0

    return report


# ---------------------------------------------------------------------------
# File walking
# ---------------------------------------------------------------------------

TEXT_EXTENSIONS = {
    ".txt", ".md", ".mdx", ".rst", ".tex", ".adoc",
    ".html", ".htm", ".xml",
    ".py", ".js", ".ts", ".jsx", ".tsx", ".rb", ".go", ".rs", ".java",
    ".css", ".scss", ".yaml", ".yml", ".toml", ".json",
    ".sh", ".bash", ".zsh",
    ".csv",
}

# Directories to always skip
SKIP_DIRS = {
    ".git", "node_modules", "__pycache__", ".venv", "venv",
    "dist", "build", ".next", ".cache", "vendor",
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
            for child in sorted(path.rglob("*")):
                if child.is_file() and child.suffix in exts:
                    if not any(skip in child.parts for skip in SKIP_DIRS):
                        result.append(child)
        else:
            print(f"warning: {p} is not a file or directory, skipping", file=sys.stderr)
    return result


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

SEVERITY_COLORS = {
    "high": "\033[91m",    # red
    "medium": "\033[93m",  # yellow
    "low": "\033[90m",     # gray
}
RESET = "\033[0m"
BOLD = "\033[1m"


def format_severity(sev: str, use_color: bool) -> str:
    if use_color:
        return f"{SEVERITY_COLORS[sev]}{sev:>6}{RESET}"
    return f"{sev:>6}"


def print_report(report: FileReport, use_color: bool, verbose: bool) -> None:
    if not report.findings:
        return

    header = f"{BOLD}{report.path}{RESET}" if use_color else report.path
    print(f"\n{header}  (slop score: {report.slop_score:.1f}, {report.word_count} words)")

    findings = report.findings
    if not verbose:
        # In non-verbose mode, skip low-severity individual findings
        findings = [f for f in findings if f.severity != "low"]

    for f in sorted(findings, key=lambda x: (x.line, x.severity)):
        sev = format_severity(f.severity, use_color)
        loc = f"  {f.line:>4}:" if f.line > 0 else "     "
        text_preview = f'  "{f.text}"' if f.text else ""
        print(f"  {loc} [{sev}] {f.message}{text_preview}")


def print_summary(reports: list[FileReport], use_color: bool) -> None:
    flagged = [r for r in reports if r.has_slop]
    if not flagged:
        print("\nNo slop detected.")
        return

    print(f"\n{'─' * 60}")
    print(f"{'Files scanned:':<30} {len(reports)}")
    print(f"{'Files with slop:':<30} {len(flagged)}")

    total_findings = sum(len(r.findings) for r in flagged)
    high = sum(1 for r in flagged for f in r.findings if f.severity == "high")
    med = sum(1 for r in flagged for f in r.findings if f.severity == "medium")
    low = sum(1 for r in flagged for f in r.findings if f.severity == "low")
    print(f"{'Total findings:':<30} {total_findings} ({high} high, {med} medium, {low} low)")

    worst = sorted(flagged, key=lambda r: r.slop_score, reverse=True)[:5]
    if len(worst) > 1:
        print(f"\nWorst offenders:")
        for r in worst:
            print(f"  {r.slop_score:>6.1f}  {r.path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
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
    parser.add_argument("paths", nargs="*", default=["-"],
                        help="files or directories to scan (- for stdin)")
    parser.add_argument("--json", metavar="FILE",
                        help="write JSON report to FILE")
    parser.add_argument("--threshold", type=float, default=0.0,
                        help="minimum slop score to report a file (default: 0)")
    parser.add_argument("--no-color", action="store_true",
                        help="disable colored output")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="show low-severity findings too")
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
            print_report(r, use_color, args.verbose)

    print_summary(reports, use_color)

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
