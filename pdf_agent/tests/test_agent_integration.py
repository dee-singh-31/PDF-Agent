import json
from datetime import date
from pathlib import Path

import pytest

from pdf_agent.application.agent import ExpiryAgent
from pdf_agent.application.date_candidate_extractor import DateCandidateExtractor
from pdf_agent.application.expiry_validator import ExpiryCandidateValidator
from pdf_agent.infrastructure.pdf_reader import PdfTextReader

FIXTURES_DIR = Path(__file__).parent / "fixtures"
FIXTURE_PDFS = sorted(FIXTURES_DIR.glob("*.pdf"))


class UnusedOCR:
    def extract(self, pdf_path):
        raise AssertionError("OCR should not be needed for a text-based PDF")


class UnusedLLM:
    def extract_expiry(self, pages):
        raise AssertionError(
            "LLM should not be needed when the rule-based extractor succeeds"
        )


def build_agent() -> ExpiryAgent:
    return ExpiryAgent(
        pdf_reader=PdfTextReader(),
        ocr=UnusedOCR(),
        llm=UnusedLLM(),
        validator=ExpiryCandidateValidator(),
        date_extractor=DateCandidateExtractor(),
    )


def load_expected(pdf_path: Path) -> dict | None:
    expected_path = pdf_path.with_suffix(".json")

    if not expected_path.exists():
        return None

    return json.loads(expected_path.read_text())


@pytest.mark.parametrize("pdf_path", FIXTURE_PDFS, ids=lambda p: p.name)
def test_fixture_pdf_matches_expected_result(pdf_path):
    result = build_agent().run(str(pdf_path))

    expected = load_expected(pdf_path)

    if expected is None:
        return

    if expected["expiry_date"] is None:
        assert result.expiry_date is None
        return

    assert result.expiry_date == date.fromisoformat(expected["expiry_date"])

    if "extraction_method" in expected:
        assert result.evidence is not None
        assert result.evidence.extraction_method == expected["extraction_method"]
