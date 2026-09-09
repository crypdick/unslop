"""Human-readable terminal reports for scanner findings."""

from slop_scanner import FileReport

SEVERITY_COLORS = {
    "high": "\033[91m",  # red
    "medium": "\033[93m",  # yellow
    "low": "\033[90m",  # gray
}
RESET = "\033[0m"
BOLD = "\033[1m"


def format_severity(sev: str, *, use_color: bool) -> str:
    if use_color:
        return f"{SEVERITY_COLORS[sev]}{sev:>6}{RESET}"
    return f"{sev:>6}"


def print_report(report: FileReport, *, use_color: bool, verbose: bool) -> None:
    if not report.findings:
        return

    header = f"{BOLD}{report.path}{RESET}" if use_color else report.path
    print(f"\n{header}  (slop score: {report.slop_score:.1f}, {report.word_count} words)")

    findings = report.findings
    if not verbose:
        # In non-verbose mode, skip low-severity individual findings
        findings = [f for f in findings if f.severity != "low"]

    for f in sorted(findings, key=lambda x: (x.line, x.severity)):
        sev = format_severity(f.severity, use_color=use_color)
        loc = f"  {f.line:>4}:" if f.line > 0 else "     "
        text_preview = f'  "{f.text}"' if f.text else ""
        print(f"  {loc} [{sev}] {f.message}{text_preview}")


def print_summary(reports: list[FileReport]) -> None:
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
        print("\nWorst offenders:")
        for r in worst:
            print(f"  {r.slop_score:>6.1f}  {r.path}")
