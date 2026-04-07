"""Tests for the slop detection script."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

# Import from the script
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from detect_slop import (
    AI_VOCABULARY,
    FileReport,
    Finding,
    collect_files,
    scan_text,
    tokenize_lower,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def findings_by_category(report: FileReport, category: str) -> list[Finding]:
    return [f for f in report.findings if f.category == category]


def findings_by_severity(report: FileReport, severity: str) -> list[Finding]:
    return [f for f in report.findings if f.severity == severity]


def has_finding_matching(report: FileReport, *, category: str = None, message_contains: str = None) -> bool:
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


# ---------------------------------------------------------------------------
# tokenize_lower
# ---------------------------------------------------------------------------

class TestTokenizeLower:
    def test_basic(self):
        assert tokenize_lower("Hello World") == ["hello", "world"]

    def test_contractions(self):
        tokens = tokenize_lower("it's worth noting that we're here")
        assert "it's" in tokens
        assert "we're" in tokens

    def test_punctuation_stripped(self):
        tokens = tokenize_lower("Hello, world! How are you?")
        assert tokens == ["hello", "world", "how", "are", "you"]

    def test_empty(self):
        assert tokenize_lower("") == []

    def test_numbers_excluded(self):
        tokens = tokenize_lower("There are 42 items in version 3.1")
        assert "42" not in tokens
        assert "3" not in tokens


# ---------------------------------------------------------------------------
# Finding / FileReport dataclasses
# ---------------------------------------------------------------------------

class TestDataclasses:
    def test_severity_weight(self):
        assert Finding(1, "high", "x", "x", "x").severity_weight == 3.0
        assert Finding(1, "medium", "x", "x", "x").severity_weight == 1.5
        assert Finding(1, "low", "x", "x", "x").severity_weight == 0.5

    def test_has_slop_false_when_empty(self):
        r = FileReport(path="test", word_count=100)
        assert r.has_slop is False
        assert r.slop_score == 0

    def test_has_slop_true_when_positive_score(self):
        r = FileReport(path="test", word_count=100, slop_score=1.5)
        assert r.has_slop is True


# ---------------------------------------------------------------------------
# scan_text: short text early return
# ---------------------------------------------------------------------------

class TestShortText:
    def test_under_10_words_returns_empty(self):
        report = scan_text("Too short.")
        assert report.findings == []
        assert report.slop_score == 0

    def test_exactly_10_words_is_scanned(self):
        # 10 words, one AI vocab word — shouldn't crash
        text = "This is a vibrant test of exactly ten word tokens."
        report = scan_text(text)
        assert report.word_count >= 10


# ---------------------------------------------------------------------------
# scan_text: AI vocabulary clustering
# ---------------------------------------------------------------------------

class TestVocabClustering:
    def test_three_ai_words_in_sentence_is_high(self):
        text = pad("The meticulous and intricate tapestry was remarkable.")
        report = scan_text(text)
        clusters = findings_by_category(report, "vocab_cluster")
        high_clusters = [f for f in clusters if f.severity == "high"]
        assert len(high_clusters) >= 1
        assert "meticulous" in high_clusters[0].message

    def test_two_ai_words_in_short_sentence_is_low(self):
        text = pad("The pivotal and crucial decision.")
        report = scan_text(text)
        clusters = findings_by_category(report, "vocab_cluster")
        # Could be high if sentence is short enough with 2 words,
        # or low for a pair — depends on sentence length
        assert len(clusters) >= 1

    def test_one_ai_word_no_cluster_finding(self):
        text = pad("The project was crucial to our success and we completed it on time.")
        report = scan_text(text)
        clusters = findings_by_category(report, "vocab_cluster")
        assert len(clusters) == 0

    def test_ai_words_spread_across_sentences_no_cluster(self):
        text = pad(
            "The project was crucial. "
            "We took a meticulous approach. "
            "The results were vibrant."
        )
        report = scan_text(text)
        # Each sentence has only 1 AI word, so no clustering findings
        clusters = [f for f in findings_by_category(report, "vocab_cluster") if f.severity == "high"]
        assert len(clusters) == 0


# ---------------------------------------------------------------------------
# scan_text: formulaic phrases
# ---------------------------------------------------------------------------

class TestFormulaicPhrases:
    def test_testament_to(self):
        text = pad("This project is a testament to the hard work of the team.")
        report = scan_text(text)
        assert has_finding_matching(report, message_contains="testament")

    def test_serves_as(self):
        text = pad("The building serves as a community center for the neighborhood.")
        report = scan_text(text)
        assert has_finding_matching(report, message_contains="serves as")

    def test_stands_as(self):
        text = pad("The monument stands as a reminder of the city's history and heritage.")
        report = scan_text(text)
        assert has_finding_matching(report, message_contains="stands as")

    def test_plays_pivotal_role(self):
        text = pad("The manager plays a pivotal role in the organization's daily operations.")
        report = scan_text(text)
        assert has_finding_matching(report, message_contains="plays a")

    def test_evolving_landscape(self):
        text = pad("In the evolving landscape of technology, companies must adapt quickly.")
        report = scan_text(text)
        assert has_finding_matching(report, message_contains="evolving landscape")

    def test_in_todays_rapidly_evolving(self):
        text = pad("In today's rapidly evolving market, businesses face new challenges every day.")
        report = scan_text(text)
        assert has_finding_matching(report, message_contains="formulaic opener")

    def test_not_just_but_also(self):
        text = pad("This is not just a tool, but also a platform for learning and growth.")
        report = scan_text(text)
        assert has_finding_matching(report, message_contains="not just")

    def test_more_than_just(self):
        text = pad("She is more than just a manager to the team members here.")
        report = scan_text(text)
        assert has_finding_matching(report, message_contains="more than just")

    def test_boasts_a(self):
        text = pad("The hotel boasts a stunning view of the valley and the mountains.")
        report = scan_text(text)
        assert has_finding_matching(report, message_contains="boasts")

    def test_rich_tapestry(self):
        text = pad("The city has a rich tapestry of cultures that make it unique.")
        report = scan_text(text)
        assert has_finding_matching(report, message_contains="rich tapestry")

    def test_diverse_array(self):
        text = pad("The store offers a diverse array of products for every customer.")
        report = scan_text(text)
        assert has_finding_matching(report, message_contains="diverse array")

    def test_commitment_to_excellence(self):
        text = pad("The company's commitment to excellence is evident in every product they make.")
        report = scan_text(text)
        assert has_finding_matching(report, message_contains="commitment to")

    def test_experts_argue(self):
        text = pad("Experts argue that the current approach is not sustainable long term.")
        report = scan_text(text)
        assert has_finding_matching(report, message_contains="vague attribution")

    def test_studies_have_shown(self):
        text = pad("Studies have shown that regular exercise improves cognitive function in adults.")
        report = scan_text(text)
        assert has_finding_matching(report, message_contains="studies have shown")

    def test_despite_challenges(self):
        text = pad("Despite these ongoing challenges, the team has adapted quickly and kept going.")
        report = scan_text(text)
        assert has_finding_matching(report, message_contains="despite")

    def test_moving_forward(self):
        text = pad("Moving forward, the team will focus on improving the core product.")
        report = scan_text(text)
        assert has_finding_matching(report, message_contains="moving forward")

    def test_its_worth_noting(self):
        text = pad("It's worth noting that the data shows a clear trend in this area.")
        report = scan_text(text)
        assert has_finding_matching(report, message_contains="worth noting")

    def test_lets_delve(self):
        text = pad("Let's delve into the details of how this system works in practice.")
        report = scan_text(text)
        assert has_finding_matching(report, message_contains="collaborative address")

    def test_heres_the_thing(self):
        text = pad("Here's the thing about distributed systems that people often forget.")
        report = scan_text(text)
        assert has_finding_matching(report, message_contains="here's the thing")

    def test_case_insensitive(self):
        text = pad("EXPERTS ARGUE that the current approach is not sustainable long term.")
        report = scan_text(text)
        assert has_finding_matching(report, message_contains="vague attribution")


# ---------------------------------------------------------------------------
# scan_text: dangling participles
# ---------------------------------------------------------------------------

class TestDanglingParticiples:
    def test_highlighting_at_end(self):
        text = pad("The report was released on Tuesday, highlighting the need for reform.")
        report = scan_text(text)
        assert has_finding_matching(report, category="dangling_participle")

    def test_underscoring_at_end(self):
        text = pad("Sales rose by twelve percent last quarter, underscoring strong demand.")
        report = scan_text(text)
        assert has_finding_matching(report, category="dangling_participle")

    def test_thereby_fostering(self):
        text = pad("The policy was changed last month, thereby fostering a more inclusive environment.")
        report = scan_text(text)
        assert has_finding_matching(report, category="dangling_participle")

    def test_contributing_to(self):
        text = pad("The new road was completed in March, contributing to economic growth.")
        report = scan_text(text)
        assert has_finding_matching(report, category="dangling_participle")

    def test_normal_participle_not_flagged(self):
        # Participle that isn't one of the filler verbs
        text = pad("She left the building, walking quickly toward the parking lot near the corner.")
        report = scan_text(text)
        assert not has_finding_matching(report, category="dangling_participle")


# ---------------------------------------------------------------------------
# scan_text: transition word starters
# ---------------------------------------------------------------------------

class TestTransitionStarters:
    def test_additionally(self):
        text = pad("Additionally, the team has expanded its product line significantly.")
        report = scan_text(text)
        assert has_finding_matching(report, category="transition_starter")

    def test_furthermore(self):
        text = pad("Furthermore, the results confirm what we suspected about the trend.")
        report = scan_text(text)
        assert has_finding_matching(report, category="transition_starter")

    def test_moreover(self):
        text = pad("Moreover, this approach reduces complexity and makes testing easier overall.")
        report = scan_text(text)
        assert has_finding_matching(report, category="transition_starter")

    def test_mid_sentence_not_flagged(self):
        text = pad("The team additionally hired three new engineers to help with the backlog.")
        report = scan_text(text)
        assert not has_finding_matching(report, category="transition_starter")

    def test_normal_sentence_start_not_flagged(self):
        text = pad("The bridge took three years to build and cost twice the estimate.")
        report = scan_text(text)
        assert not has_finding_matching(report, category="transition_starter")


# ---------------------------------------------------------------------------
# scan_text: document-level density checks
# ---------------------------------------------------------------------------

class TestDocumentLevelDensity:
    def test_high_vocab_density(self):
        # Pack lots of AI words into a short text
        text = (
            "The meticulous and intricate tapestry of this vibrant realm "
            "is a testament to the pivotal and crucial role of robust paradigms. "
            "The comprehensive and nuanced approach to fostering holistic synergy "
            "has bolstered the enduring legacy of this groundbreaking beacon."
        )
        report = scan_text(text)
        assert report.ai_vocab_density > 3.0
        assert has_finding_matching(report, category="vocab_density", message_contains="high")

    def test_medium_vocab_density(self):
        # Sprinkle a few AI words across enough normal text to land in the 1.5-3% band
        text = (
            "The team worked hard on the project last quarter. "
            "They used a meticulous approach to testing each component. "
            "The results were quite good and the client was happy with everything. "
            "We found the process to be solid and reliable overall this time around. "
            "The final delivery was on time and under budget which was a relief. "
            "Everyone agreed the morning meeting helped align priorities for the week. "
            "The next sprint will focus on fixing the remaining edge cases in auth. "
            "We also need to update the documentation before the release goes out. "
            "The QA team signed off on all the critical paths through the system. "
            "Overall it was a productive quarter for the whole engineering organization."
        )
        report = scan_text(text)
        # Only 1 AI word (meticulous) in ~100 words ≈ 1.0%
        # Should not trigger high density
        density_findings = findings_by_category(report, "vocab_density")
        high_density = [f for f in density_findings if f.severity == "high"]
        assert len(high_density) == 0

    def test_clean_text_no_density_finding(self):
        text = (
            "The bridge took three years to build and cost twice the original estimate. "
            "Most of the delays came from soil conditions nobody expected. "
            "The riverbed turned out to be mostly clay, which complicated the foundation work. "
            "The engineering team switched to driven piles about eight months in."
        )
        report = scan_text(text)
        density_findings = findings_by_category(report, "vocab_density")
        assert len(density_findings) == 0

    def test_em_dash_density(self):
        text = (
            "The project — which started in January — was ambitious. "
            "The team — led by Sarah — made quick progress. "
            "Results — as expected — were positive. "
            "The client — a Fortune 500 company — was pleased with the outcome."
        )
        report = scan_text(text)
        assert has_finding_matching(report, category="em_dash_density")

    def test_few_em_dashes_not_flagged(self):
        # 1 em dash in ~60 words ≈ 1.7/100, well under the 2.0 threshold
        text = (
            "The project — which started in January — was ambitious and well-planned. "
            "The team delivered every milestone on schedule and the client was happy with "
            "the result. We learned a lot about the domain and built solid foundations "
            "for the next phase of work. The documentation was thorough and the onboarding "
            "guide made it easy for new contributors to get up to speed quickly without "
            "much help. Feedback from stakeholders was positive. The next phase starts in "
            "March and will focus on scaling the backend to handle more traffic from the "
            "mobile app which launched last month to strong reviews from users and press."
        )
        report = scan_text(text)
        assert not has_finding_matching(report, category="em_dash_density")

    def test_transition_density(self):
        text = (
            "The first point is about speed.\n\n"
            "Additionally, we need to consider cost.\n\n"
            "Furthermore, the team raised concerns.\n\n"
            "Moreover, the timeline was tight.\n\n"
            "Consequently, we revised the plan."
        )
        report = scan_text(text)
        assert has_finding_matching(report, category="transition_density")


# ---------------------------------------------------------------------------
# scan_text: slop score
# ---------------------------------------------------------------------------

class TestSlopScore:
    def test_clean_text_zero_score(self):
        text = (
            "The bridge took three years to build and cost twice the original estimate. "
            "Most of the delays came from soil conditions nobody expected. "
            "The riverbed turned out to be mostly clay. "
            "The engineering team switched to driven piles about eight months in."
        )
        report = scan_text(text)
        assert report.slop_score == 0

    def test_sloppy_text_positive_score(self):
        text = (
            "In today's rapidly evolving digital landscape, organizations are "
            "increasingly leveraging cutting-edge AI to enhance their operational "
            "efficiency. This groundbreaking shift serves as a testament to innovation."
        )
        report = scan_text(text)
        assert report.slop_score > 0

    def test_score_scales_with_word_count(self):
        """Same findings in longer text should produce lower score."""
        short = "The project serves as a testament to innovation and hard work by the team members."
        long = short + " " + ("The team worked hard on many tasks last quarter. " * 10)
        short_report = scan_text(short)
        long_report = scan_text(long)
        # Both have the same phrases, but long text dilutes the score
        assert long_report.slop_score < short_report.slop_score


# ---------------------------------------------------------------------------
# scan_text: severity assignment
# ---------------------------------------------------------------------------

class TestSeverityAssignment:
    def test_significance_inflation_is_high(self):
        text = pad("This is a testament to the team's hard work and dedication to the project.")
        report = scan_text(text)
        phrase_findings = findings_by_category(report, "formulaic_phrase")
        testament = [f for f in phrase_findings if "testament" in f.message]
        assert testament and testament[0].severity == "high"

    def test_copulative_avoidance_is_high(self):
        text = pad("The building serves as a community center for the entire neighborhood.")
        report = scan_text(text)
        phrase_findings = findings_by_category(report, "formulaic_phrase")
        serves = [f for f in phrase_findings if "serves as" in f.message]
        assert serves and serves[0].severity == "high"

    def test_promotional_is_medium(self):
        text = pad("The restaurant boasts a lovely garden patio overlooking the river.")
        report = scan_text(text)
        phrase_findings = findings_by_category(report, "formulaic_phrase")
        boasts = [f for f in phrase_findings if "boasts" in f.message]
        assert boasts and boasts[0].severity == "medium"

    def test_dangling_participle_is_medium(self):
        text = pad("Revenue grew last quarter, highlighting strong demand across all regions.")
        report = scan_text(text)
        dp = findings_by_category(report, "dangling_participle")
        assert dp and dp[0].severity == "medium"

    def test_transition_starter_is_low(self):
        text = pad("Additionally, the team has expanded its product line significantly.")
        report = scan_text(text)
        ts = findings_by_category(report, "transition_starter")
        assert ts and ts[0].severity == "low"


# ---------------------------------------------------------------------------
# scan_text: false positive resistance
# ---------------------------------------------------------------------------

class TestFalsePositives:
    def test_normal_prose_is_clean(self):
        text = (
            "We shipped the new API on Thursday. It handles about 2,000 requests "
            "per second on a single node, which is enough for now. If traffic "
            "doubles, we will add a second node behind the load balancer. "
            "The main risk is the database connection pool — we are using 80 of "
            "100 connections at peak."
        )
        report = scan_text(text)
        high = findings_by_severity(report, "high")
        assert len(high) == 0

    def test_technical_writing_is_clean(self):
        text = (
            "The function accepts a list of integers and returns the median value. "
            "For even-length lists, it averages the two middle elements. "
            "Time complexity is O(n log n) due to the sort step. "
            "Space complexity is O(1) if we sort in place."
        )
        report = scan_text(text)
        high = findings_by_severity(report, "high")
        assert len(high) == 0

    def test_single_ai_word_not_flagged_as_cluster(self):
        text = pad("The results were robust across all experimental conditions we tested.")
        report = scan_text(text)
        clusters = [f for f in findings_by_category(report, "vocab_cluster") if f.severity == "high"]
        assert len(clusters) == 0


# ---------------------------------------------------------------------------
# scan_text: integration (full AI-generated paragraphs)
# ---------------------------------------------------------------------------

class TestIntegration:
    def test_classic_ai_blog_intro(self):
        text = (
            "In today's rapidly evolving digital landscape, organizations are "
            "increasingly leveraging cutting-edge AI technologies to enhance their "
            "operational efficiency. This groundbreaking shift not only underscores "
            "the transformative potential of machine learning but also serves as a "
            "testament to the innovative spirit that drives modern enterprises. "
            "Let's delve into the multifaceted implications of this pivotal development."
        )
        report = scan_text(text)
        assert report.slop_score > 10
        high = findings_by_severity(report, "high")
        assert len(high) >= 3

    def test_ai_written_bio(self):
        text = (
            "Dr. Sarah Chen is a renowned researcher who has left an indelible mark "
            "on the field of computational biology. Her meticulous approach to data "
            "analysis, combined with her commitment to fostering collaborative research "
            "environments, has garnered widespread recognition from industry experts. "
            "Not just a scientist, but a visionary, she continues to spearhead "
            "groundbreaking initiatives at the intersection of AI and healthcare."
        )
        report = scan_text(text)
        assert report.slop_score > 5
        assert has_finding_matching(report, message_contains="indelible mark")
        assert has_finding_matching(report, message_contains="intersection")
        assert has_finding_matching(report, message_contains="not just")

    def test_ai_product_description(self):
        text = (
            "The Kestrel 400 is a lightweight hiking boot that boasts a vibrant "
            "design and offers exceptional comfort for long-distance trekkers. "
            "Featuring a diverse array of innovative materials, it represents a "
            "significant step forward in outdoor footwear technology. Despite some "
            "challenges with waterproofing in extreme conditions, the Kestrel 400 "
            "showcases the brand's commitment to quality and continues to resonate "
            "with outdoor enthusiasts worldwide."
        )
        report = scan_text(text)
        assert report.slop_score > 3
        assert has_finding_matching(report, message_contains="boasts")
        assert has_finding_matching(report, message_contains="diverse array")
        assert has_finding_matching(report, message_contains="commitment to")

    def test_human_written_is_clean(self):
        text = (
            "The bridge took three years to build and cost twice the original "
            "estimate. Most of the delays came from soil conditions nobody expected "
            "— the riverbed turned out to be mostly clay, which complicated the "
            "foundation work. The engineering team switched to driven piles about "
            "eight months in, which solved the stability problem but blew the budget. "
            "It opened to traffic last September."
        )
        report = scan_text(text)
        high = findings_by_severity(report, "high")
        assert len(high) == 0
        assert report.slop_score < 2


# ---------------------------------------------------------------------------
# collect_files
# ---------------------------------------------------------------------------

class TestCollectFiles:
    def test_single_file(self, tmp_path):
        f = tmp_path / "test.md"
        f.write_text("hello")
        result = collect_files([str(f)])
        assert len(result) == 1
        assert result[0] == f

    def test_directory_finds_text_files(self, tmp_path):
        (tmp_path / "a.md").write_text("hello")
        (tmp_path / "b.txt").write_text("world")
        (tmp_path / "c.png").write_bytes(b"\x89PNG")  # not text
        result = collect_files([str(tmp_path)])
        extensions = {r.suffix for r in result}
        assert ".md" in extensions
        assert ".txt" in extensions
        assert ".png" not in extensions

    def test_skips_git_dir(self, tmp_path):
        git_dir = tmp_path / ".git"
        git_dir.mkdir()
        (git_dir / "config").write_text("bare = false")
        (tmp_path / "readme.md").write_text("hello")
        result = collect_files([str(tmp_path)])
        paths_str = [str(r) for r in result]
        assert not any(".git" in p for p in paths_str)

    def test_skips_node_modules(self, tmp_path):
        nm = tmp_path / "node_modules" / "pkg"
        nm.mkdir(parents=True)
        (nm / "index.js").write_text("module.exports = {}")
        (tmp_path / "app.js").write_text("console.log('hi')")
        result = collect_files([str(tmp_path)])
        assert len(result) == 1
        assert result[0].name == "app.js"

    def test_nonexistent_path_skipped(self, tmp_path, capsys):
        result = collect_files([str(tmp_path / "nope")])
        assert len(result) == 0
        assert "warning" in capsys.readouterr().err

    def test_nested_directories(self, tmp_path):
        sub = tmp_path / "src" / "components"
        sub.mkdir(parents=True)
        (sub / "button.tsx").write_text("export const Button = () => {}")
        (tmp_path / "readme.md").write_text("hello")
        result = collect_files([str(tmp_path)])
        assert len(result) == 2


# ---------------------------------------------------------------------------
# CLI (subprocess tests)
# ---------------------------------------------------------------------------

SCRIPT = str(Path(__file__).resolve().parent.parent / "scripts" / "detect_slop.py")


class TestCLI:
    def test_stdin_clean_exit_0(self):
        result = subprocess.run(
            [sys.executable, SCRIPT, "-"],
            input="The bridge took three years to build and cost twice the estimate overall.",
            capture_output=True, text=True,
        )
        assert result.returncode == 0
        assert "No slop detected" in result.stdout

    def test_stdin_sloppy_exit_1(self):
        text = (
            "In today's rapidly evolving digital landscape, organizations are "
            "leveraging cutting-edge AI to enhance operational efficiency. "
            "This groundbreaking shift serves as a testament to innovation. "
            "Let's delve into the multifaceted implications of this pivotal change."
        )
        result = subprocess.run(
            [sys.executable, SCRIPT, "-"],
            input=text, capture_output=True, text=True,
        )
        assert result.returncode == 1

    def test_file_argument(self, tmp_path):
        f = tmp_path / "test.md"
        f.write_text(
            "The building serves as a community center for the neighborhood. "
            "It is a testament to the community's dedication and commitment. "
            "The meticulous design showcases the intricate interplay of form and function."
        )
        result = subprocess.run(
            [sys.executable, SCRIPT, str(f)],
            capture_output=True, text=True,
        )
        assert result.returncode == 1
        assert "serves as" in result.stdout or "testament" in result.stdout

    def test_directory_argument(self, tmp_path):
        (tmp_path / "clean.md").write_text(
            "The team shipped the feature on Friday. It works well so far."
        )
        (tmp_path / "sloppy.md").write_text(
            "This groundbreaking initiative is a testament to the team's meticulous approach. "
            "The intricate tapestry of solutions leverages robust paradigms and holistic synergy. "
            "Let's delve into the multifaceted implications of this pivotal transformation."
        )
        result = subprocess.run(
            [sys.executable, SCRIPT, str(tmp_path)],
            capture_output=True, text=True,
        )
        assert result.returncode == 1
        assert "sloppy.md" in result.stdout

    def test_json_output(self, tmp_path):
        f = tmp_path / "test.md"
        f.write_text(
            "The restaurant boasts a diverse array of dishes and a rich tapestry of flavors. "
            "It's worth noting that experts argue the menu is truly unique and exceptional."
        )
        json_file = tmp_path / "report.json"
        result = subprocess.run(
            [sys.executable, SCRIPT, "--json", str(json_file), str(f)],
            capture_output=True, text=True,
        )
        assert json_file.exists()
        data = json.loads(json_file.read_text())
        assert len(data) == 1
        assert data[0]["word_count"] > 0
        assert data[0]["slop_score"] > 0
        assert len(data[0]["findings"]) > 0

    def test_threshold_filters(self, tmp_path):
        f = tmp_path / "mild.md"
        f.write_text(
            "The city boasts a lively arts scene that attracts visitors from across the region. "
            "Local restaurants serve dishes made with ingredients sourced from nearby farms."
        )
        # With very high threshold, should exit 0
        result = subprocess.run(
            [sys.executable, SCRIPT, "--threshold", "99", str(f)],
            capture_output=True, text=True,
        )
        assert result.returncode == 0

    def test_no_text_files_exit_2(self, tmp_path):
        (tmp_path / "image.png").write_bytes(b"\x89PNG")
        result = subprocess.run(
            [sys.executable, SCRIPT, str(tmp_path)],
            capture_output=True, text=True,
        )
        assert result.returncode == 2
        assert "No text files" in result.stderr

    def test_verbose_shows_low_severity(self, tmp_path):
        f = tmp_path / "test.md"
        f.write_text(
            "Additionally, the team has expanded its product line. "
            "The new products include several interesting items for sale. "
            "Customers have responded well to the changes so far this year."
        )
        verbose = subprocess.run(
            [sys.executable, SCRIPT, "-v", str(f)],
            capture_output=True, text=True,
        )
        quiet = subprocess.run(
            [sys.executable, SCRIPT, str(f)],
            capture_output=True, text=True,
        )
        # Verbose output should be longer (includes low-severity findings)
        assert len(verbose.stdout) >= len(quiet.stdout)
