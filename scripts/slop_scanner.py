"""Analyze text and return scored findings without performing I/O."""

import re
from dataclasses import dataclass, field
from typing import Literal

from slop_patterns import (
    AI_VOCABULARY,
    BOLD_RE,
    COMPILED_CHATBOT_ARTIFACTS,
    COMPILED_KNOWLEDGE_CUTOFFS,
    COMPILED_PHRASES,
    CURLY_QUOTES_RE,
    DANGLING_PARTICIPLE_RE,
    DECORATIVE_EMOJI_LINE_RE,
    EM_DASH_RE,
    INLINE_HEADER_ITEM_RE,
    TITLE_CASE_HEADING_RE,
    TRANSITION_STARTERS,
)

type Severity = Literal["high", "medium", "low"]


@dataclass
class Finding:
    line: int
    severity: Severity
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


def _scan_heading(stripped: str, line_num: int, report: FileReport) -> None:
    # Title case headings (markdown)
    heading_match = TITLE_CASE_HEADING_RE.match(stripped)
    if heading_match:
        title = heading_match.group(1).strip()
        # Check if most words are capitalized (skip short words)
        heading_words = title.split()
        if len(heading_words) >= 3:
            skip = {
                "a",
                "an",
                "the",
                "and",
                "or",
                "but",
                "in",
                "on",
                "at",
                "to",
                "for",
                "of",
                "with",
                "by",
                "is",
                "as",
            }
            capitalized = sum(1 for w in heading_words if w[0].isupper() or w.lower() in skip)
            if capitalized == len(heading_words):
                report.findings.append(
                    Finding(
                        line=line_num,
                        severity="low",
                        category="title_case_heading",
                        message="title case heading (AI default; most style guides use sentence case)",
                        text=stripped[:80],
                    )
                )


def _scan_line(stripped: str, line_num: int, report: FileReport) -> None:
    # Formulaic phrases
    for pattern, name in COMPILED_PHRASES:
        for match in pattern.finditer(stripped):
            report.findings.append(
                Finding(
                    line=line_num,
                    severity="high" if "significance" in name or "copulative" in name else "medium",
                    category="formulaic_phrase",
                    message=name,
                    text=match.group(0)[:80],
                )
            )

    # Pasted chatbot correspondence
    for pattern, message in COMPILED_CHATBOT_ARTIFACTS:
        for match in pattern.finditer(stripped):
            report.findings.append(
                Finding(
                    line=line_num,
                    severity="medium",
                    category="chatbot_artifact",
                    message=message,
                    text=match.group(0)[:80],
                )
            )

    # Explicit model knowledge-cutoff disclaimers
    for pattern, message in COMPILED_KNOWLEDGE_CUTOFFS:
        for match in pattern.finditer(stripped):
            report.findings.append(
                Finding(
                    line=line_num,
                    severity="medium",
                    category="knowledge_cutoff",
                    message=message,
                    text=match.group(0)[:80],
                )
            )

    # Dangling participle filler
    for match in DANGLING_PARTICIPLE_RE.finditer(stripped):
        report.findings.append(
            Finding(
                line=line_num,
                severity="medium",
                category="dangling_participle",
                message="dangling participle filler clause",
                text=match.group(0).strip()[:80],
            )
        )

    # AI vocabulary clustering (per-sentence)
    sentences = re.split(r"[.!?]+", stripped)
    for sentence in sentences:
        sent_words = tokenize_lower(sentence)
        ai_words_in_sent = [w for w in sent_words if w in AI_VOCABULARY]
        if len(ai_words_in_sent) >= 3:
            report.findings.append(
                Finding(
                    line=line_num,
                    severity="high",
                    category="vocab_cluster",
                    message=f"AI vocabulary cluster: {', '.join(ai_words_in_sent)}",
                    text=sentence.strip()[:80],
                )
            )
        elif len(ai_words_in_sent) == 2 and len(sent_words) < 20:
            report.findings.append(
                Finding(
                    line=line_num,
                    severity="low",
                    category="vocab_cluster",
                    message=f"AI vocabulary pair in short sentence: {', '.join(ai_words_in_sent)}",
                    text=sentence.strip()[:80],
                )
            )

    # Transition word starters
    if TRANSITION_STARTERS.match(stripped):
        report.findings.append(
            Finding(
                line=line_num,
                severity="low",
                category="transition_starter",
                message="sentence starts with overused transition word",
                text=stripped[:60],
            )
        )

    _scan_heading(stripped, line_num, report)

    # Curly/smart quotes
    if CURLY_QUOTES_RE.search(stripped):
        report.findings.append(
            Finding(
                line=line_num,
                severity="low",
                category="curly_quotes",
                message="curly/smart quotes (common AI artifact)",
                text=stripped[:60],
            )
        )


def _scan_document(text: str, words: list[str], report: FileReport) -> None:
    # --- Document-level analysis ---

    # AI vocabulary density
    ai_words = [w for w in words if w in AI_VOCABULARY]
    report.ai_vocab_count = len(ai_words)
    report.ai_vocab_density = (len(ai_words) / len(words)) * 100

    if report.ai_vocab_density > 1.5:
        report.findings.append(
            Finding(
                line=0,
                severity="high",
                category="vocab_density",
                message=f"high AI vocabulary density: {report.ai_vocab_density:.1f}% ({len(ai_words)} words in {len(words)})",
                text=", ".join(sorted(set(ai_words))),
            )
        )
    elif report.ai_vocab_density > 0.5:
        report.findings.append(
            Finding(
                line=0,
                severity="medium",
                category="vocab_density",
                message=f"elevated AI vocabulary density: {report.ai_vocab_density:.1f}%",
                text=", ".join(sorted(set(ai_words))),
            )
        )

    # Em dash density
    em_dashes = len(EM_DASH_RE.findall(text))
    em_dash_rate = em_dashes / (len(words) / 100)
    if em_dash_rate > 0.5:
        report.findings.append(
            Finding(
                line=0,
                severity="low",
                category="em_dash_density",
                message=f"em dash density: {em_dashes} em dashes per {len(words)} words ({em_dash_rate:.1f}/100 words)",
                text="",
            )
        )

    # Transition word density
    transition_count = len(TRANSITION_STARTERS.findall(text))
    para_count = len([p for p in text.split("\n\n") if p.strip()])
    if para_count > 2 and transition_count / para_count > 0.25:
        report.findings.append(
            Finding(
                line=0,
                severity="medium",
                category="transition_density",
                message=f"high transition word density: {transition_count}/{para_count} paragraphs start with transition words",
                text="",
            )
        )

    # Boldface density (markdown)
    bold_count = len(BOLD_RE.findall(text))
    bold_rate = bold_count / (len(words) / 100)
    if bold_rate > 1.0:
        report.findings.append(
            Finding(
                line=0,
                severity="low",
                category="bold_density",
                message=f"heavy boldface usage: {bold_count} bold spans per {len(words)} words ({bold_rate:.1f}/100 words)",
                text="",
            )
        )

    # Repeated bold-label list items
    inline_header_items = len(INLINE_HEADER_ITEM_RE.findall(text))
    if inline_header_items >= 3:
        report.findings.append(
            Finding(
                line=0,
                severity="low",
                category="inline_header_list",
                message=f"repeated inline-header list: {inline_header_items} bold-label items",
                text="",
            )
        )

    # Repeated decorative emoji in headings or list items
    decorative_emoji_lines = len(DECORATIVE_EMOJI_LINE_RE.findall(text))
    if decorative_emoji_lines >= 2:
        report.findings.append(
            Finding(
                line=0,
                severity="low",
                category="decorative_emoji",
                message=f"decorative emoji start {decorative_emoji_lines} headings/list items",
                text="",
            )
        )


def scan_text(text: str, filepath: str = "<stdin>") -> FileReport:
    """Analyze text for AI writing patterns and compute weighted findings per 100 words."""
    report = FileReport(path=filepath)
    words = tokenize_lower(text)
    report.word_count = len(words)
    if report.word_count < 10:
        return report

    for line_num, line in enumerate(text.split("\n"), start=1):
        stripped = line.strip()
        if stripped:
            _scan_line(stripped, line_num, report)
    _scan_document(text, words, report)
    raw_score = sum(f.severity_weight for f in report.findings)
    report.slop_score = raw_score / len(words) * 100
    return report
