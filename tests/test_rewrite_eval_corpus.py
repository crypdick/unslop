"""Schema and detector checks for the manual rewrite evaluation corpus."""

import json
from pathlib import Path

import pytest
from detect_slop import scan_text

ROOT = Path(__file__).resolve().parent.parent
CORPUS_PATH = ROOT / "evals" / "rewrite_cases.json"

with CORPUS_PATH.open(encoding="utf-8") as corpus_file:
    CORPUS = json.load(corpus_file)

CASES = CORPUS["cases"]


def test_corpus_schema_and_unique_ids():
    assert CORPUS["schema_version"] == 1
    assert len(CASES) >= 5

    ids = [case["id"] for case in CASES]
    assert len(ids) == len(set(ids))

    for case in CASES:
        assert case["focus"]
        assert case["input"]
        assert case["must_preserve"]
        assert case["must_avoid"]
        assert "detector_categories" in case


@pytest.mark.parametrize("case", CASES, ids=lambda case: case["id"])
def test_rewrite_constraints_are_grounded_in_input(case):
    for required_text in case["must_preserve"]:
        assert required_text in case["input"]
    for unwanted_text in case["must_avoid"]:
        assert unwanted_text in case["input"]


@pytest.mark.parametrize("case", CASES, ids=lambda case: case["id"])
def test_detector_covers_declared_categories(case):
    report = scan_text(case["input"], filepath=case["id"])
    categories = {finding.category for finding in report.findings}
    assert set(case["detector_categories"]) <= categories
