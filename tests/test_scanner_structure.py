"""Behavior checks for the writing-pattern scanner."""

import pytest
from detect_slop import scan_text

from tests.scanner_support import findings_by_category, has_finding_matching, pad


class TestChatbotArtifacts:
    @pytest.mark.parametrize(
        "artifact",
        [
            "I hope this helps!",
            "Let me know if you'd like more detail.",
            "Let me know if you\u2019d like more detail.",
            "Would you like me to continue?",
            "As an AI language model, I cannot verify that claim.",
        ],
    )
    def test_chatbot_artifact_flagged(self, artifact):
        report = scan_text(pad(artifact))
        assert has_finding_matching(report, category="chatbot_artifact")

    def test_normal_request_not_flagged(self):
        report = scan_text(pad("Let me know tomorrow whether the migration finished on time."))
        assert not has_finding_matching(report, category="chatbot_artifact")


class TestKnowledgeCutoffArtifacts:
    @pytest.mark.parametrize(
        "artifact",
        [
            "Up to my last training update, the company had three offices.",
            "As of my last knowledge cutoff, the package was still experimental.",
            "My knowledge cutoff was June, so I cannot confirm the release.",
            "I don\u2019t have access to real-time information about the current price.",
        ],
    )
    def test_knowledge_cutoff_flagged(self, artifact):
        report = scan_text(pad(artifact))
        assert has_finding_matching(report, category="knowledge_cutoff")

    def test_source_specific_uncertainty_not_flagged(self):
        text = pad("The archived report does not give an exact opening date for the office.")
        report = scan_text(text)
        assert not has_finding_matching(report, category="knowledge_cutoff")


# ---------------------------------------------------------------------------
# scan_text: title case headings
# ---------------------------------------------------------------------------


class TestTitleCaseHeadings:
    def test_title_case_flagged(self):
        text = pad("## Global Context: Critical Mineral Demand And Supply Chain Issues")
        report = scan_text(text)
        assert has_finding_matching(report, category="title_case_heading")

    def test_sentence_case_not_flagged(self):
        text = pad("## Global context: critical mineral demand and supply chain issues")
        report = scan_text(text)
        assert not has_finding_matching(report, category="title_case_heading")

    def test_short_heading_not_flagged(self):
        # Headings with fewer than 3 words are ignored (too ambiguous)
        text = "## Key Points\n\nThe bridge took three years to build and cost twice the estimate overall."
        report = scan_text(text)
        assert not has_finding_matching(report, category="title_case_heading")


# ---------------------------------------------------------------------------
# scan_text: curly quotes
# ---------------------------------------------------------------------------


class TestCurlyQuotes:
    def test_curly_quotes_flagged(self):
        text = pad("The \u201cbest\u201d approach is to use straight quotes in plain text files.")
        report = scan_text(text)
        assert has_finding_matching(report, category="curly_quotes")

    def test_curly_apostrophe_flagged(self):
        text = pad("It\u2019s important to use consistent quotation marks throughout the text.")
        report = scan_text(text)
        assert has_finding_matching(report, category="curly_quotes")

    def test_straight_quotes_not_flagged(self):
        text = pad('The "best" approach is to keep things simple and direct overall.')
        report = scan_text(text)
        assert not has_finding_matching(report, category="curly_quotes")


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
        # 1 AI word (meticulous) in ~100 words ≈ 1.0%, in the medium band (0.5-1.5%)
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
        density_findings = findings_by_category(report, "vocab_density")
        # Should be medium, not high
        high_density = [f for f in density_findings if f.severity == "high"]
        assert len(high_density) == 0
        medium_density = [f for f in density_findings if f.severity == "medium"]
        assert len(medium_density) == 1

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

    def test_single_em_dash_in_long_text_not_flagged(self):
        # 1 em dash in ~200 words ≈ 0.5/100, at the threshold boundary
        text = (
            "The project started in January and was ambitious from the start. "
            "The team delivered every milestone on schedule and the client was happy with "
            "the result. We learned a lot about the domain and built solid foundations "
            "for the next phase of work. The documentation was thorough and the onboarding "
            "guide made it easy for new contributors to get up to speed quickly without "
            "much help. Feedback from stakeholders was positive. The next phase starts in "
            "March and will focus on scaling the backend to handle more traffic from the "
            "mobile app which launched last month to strong reviews from users and press. "
            "The database migration went smoothly and the new schema handles the increased "
            "load without any issues. We also set up monitoring dashboards that track the "
            "key performance indicators the product team cares about. The CI pipeline now "
            "runs in under four minutes, down from twelve — which has made the team much "
            "more productive during code review cycles. Overall it was a strong quarter "
            "for the whole engineering organization and we are all looking forward to "
            "continuing this positive momentum well into the next one. The hiring pipeline "
            "is also healthy with several strong candidates in the final interview rounds "
            "for the two open backend positions we posted last month."
        )
        report = scan_text(text)
        assert not has_finding_matching(report, category="em_dash_density")

    def test_few_em_dashes_flagged_at_lower_threshold(self):
        # 2 em dashes in ~80 words ≈ 2.5/100, well above the 0.5 threshold
        text = (
            "The project — which started in January — was ambitious and well-planned. "
            "The team delivered every milestone on schedule and the client was happy with "
            "the result. We learned a lot about the domain and built solid foundations "
            "for the next phase of work that kicks off in March."
        )
        report = scan_text(text)
        assert has_finding_matching(report, category="em_dash_density")

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

    def test_bold_density(self):
        text = (
            "The **first** step is to **identify** the problem. "
            "Then **analyze** the **root cause** and **document** your findings. "
            "Finally, **implement** the **solution** and **verify** results."
        )
        report = scan_text(text)
        assert has_finding_matching(report, category="bold_density")

    def test_sparse_bold_not_flagged(self):
        # 1 bold in 100+ words ≈ <1.0/100, below threshold
        text = (
            "The project has a single **important** constraint: the deadline. "
            "Everything else is negotiable. The team has been working on this for "
            "three months and we expect to ship in two more weeks at the latest. "
            "The backend migration is on track and the database schema has been "
            "finalized. We still need to update the documentation before the release "
            "goes out, but that should only take a day or two at most. The QA team "
            "has already signed off on all the critical user flows and the staging "
            "environment is stable. We ran load tests last week and the system "
            "handled twice our expected peak traffic without any issues."
        )
        report = scan_text(text)
        assert not has_finding_matching(report, category="bold_density")

    def test_repeated_inline_header_list_flagged(self):
        text = (
            "- **Performance:** The cache reduced median response time.\n"
            "- **Security:** Hardware keys are now required for administrators.\n"
            "- **Usability:** The signup form has two fewer fields."
        )
        report = scan_text(text)
        assert has_finding_matching(report, category="inline_header_list")

    def test_two_inline_header_items_not_flagged(self):
        text = (
            "- **Owner:** Mina runs the rollback drill on Friday.\n"
            "- **Deadline:** The release goes out on September eighth."
        )
        report = scan_text(text)
        assert not has_finding_matching(report, category="inline_header_list")

    def test_repeated_decorative_emoji_flagged(self):
        text = (
            "## 🚀 Launch\nThe release goes out after the database migration.\n\n"
            "## ✅ Next step\nMina runs the rollback drill on Friday."
        )
        report = scan_text(text)
        assert has_finding_matching(report, category="decorative_emoji")

    def test_single_emoji_heading_not_flagged(self):
        text = "## ✅ Status\nThe migration finished on Tuesday after forty minutes of maintenance."
        report = scan_text(text)
        assert not has_finding_matching(report, category="decorative_emoji")


# ---------------------------------------------------------------------------
# scan_text: slop score
# ---------------------------------------------------------------------------
