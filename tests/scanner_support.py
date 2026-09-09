"""Finding queries and sample-text padding for scanner tests."""

from detect_slop import FileReport, Finding, tokenize_lower


def findings_by_category(report: FileReport, category: str) -> list[Finding]:
    return [f for f in report.findings if f.category == category]


def findings_by_severity(report: FileReport, severity: str) -> list[Finding]:
    return [f for f in report.findings if f.severity == severity]


def has_finding_matching(
    report: FileReport, *, category: str | None = None, message_contains: str | None = None
) -> bool:
    for f in report.findings:
        if category and f.category != category:
            continue
        if message_contains and message_contains.lower() not in f.message.lower():
            continue
        return True
    return False


# Pad short text so it clears the 10-word minimum
def pad(text: str, n: int = 20) -> str:
    """Append filler words to get past the 10-word minimum."""
    words = tokenize_lower(text)
    if len(words) >= n:
        return text
    padding = " ".join(["the"] * (n - len(words)))
    return text + " " + padding
