"""Behavior checks for the writing-pattern scanner."""

from detect_slop import scan_text

from tests.scanner_support import findings_by_category, findings_by_severity, has_finding_matching, pad


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
        assert testament
        assert testament[0].severity == "high"

    def test_copulative_avoidance_is_high(self):
        text = pad("The building serves as a community center for the entire neighborhood.")
        report = scan_text(text)
        phrase_findings = findings_by_category(report, "formulaic_phrase")
        serves = [f for f in phrase_findings if "serves as" in f.message]
        assert serves
        assert serves[0].severity == "high"

    def test_promotional_is_medium(self):
        text = pad("The restaurant boasts a lovely garden patio overlooking the river.")
        report = scan_text(text)
        phrase_findings = findings_by_category(report, "formulaic_phrase")
        boasts = [f for f in phrase_findings if "boasts" in f.message]
        assert boasts
        assert boasts[0].severity == "medium"

    def test_dangling_participle_is_medium(self):
        text = pad("Revenue grew last quarter, highlighting strong demand across all regions.")
        report = scan_text(text)
        dp = findings_by_category(report, "dangling_participle")
        assert dp
        assert dp[0].severity == "medium"

    def test_transition_starter_is_low(self):
        text = pad("Additionally, the team has expanded its product line significantly.")
        report = scan_text(text)
        ts = findings_by_category(report, "transition_starter")
        assert ts
        assert ts[0].severity == "low"


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
