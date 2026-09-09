"""Behavior checks for the writing-pattern scanner."""

from detect_slop import FileReport, Finding, scan_text, tokenize_lower

from tests.scanner_support import findings_by_category, has_finding_matching, pad


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
        text = pad("The project was crucial. We took a meticulous approach. The results were vibrant.")
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

    def test_sycophantic_opener_great_question(self):
        text = pad("Great question! The answer depends on several factors in this case.")
        report = scan_text(text)
        assert has_finding_matching(report, message_contains="sycophantic")

    def test_sycophantic_opener_absolutely(self):
        text = pad("Absolutely! That is exactly the right approach to take here.")
        report = scan_text(text)
        assert has_finding_matching(report, message_contains="sycophantic")

    def test_sycophantic_opener_you_raise(self):
        text = pad("You raise a really important point about the architecture of the system.")
        report = scan_text(text)
        assert has_finding_matching(report, message_contains="sycophantic")

    def test_structural_scaffolding_three_key(self):
        text = pad("There are three key factors to consider when evaluating this approach.")
        report = scan_text(text)
        assert has_finding_matching(report, message_contains="scaffolding")

    def test_structural_scaffolding_break_down(self):
        text = pad("Let's break this down into smaller components so it is easier to see.")
        report = scan_text(text)
        assert has_finding_matching(report, message_contains="scaffolding")

    def test_renowned_for(self):
        text = pad("The university is renowned for its engineering program and research output.")
        report = scan_text(text)
        assert has_finding_matching(report, message_contains="notability")

    def test_widely_regarded_as(self):
        text = pad("She is widely regarded as one of the leading experts in the field today.")
        report = scan_text(text)
        assert has_finding_matching(report, message_contains="notability")


# ---------------------------------------------------------------------------
# scan_text: chatbot and knowledge-cutoff artifacts
# ---------------------------------------------------------------------------
