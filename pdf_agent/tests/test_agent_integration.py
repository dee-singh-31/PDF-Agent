from datetime import date
from pathlib import Path

from pdf_agent.application.agent import ExpiryAgent
from pdf_agent.application.date_candidate_extractor import DateCandidateExtractor
from pdf_agent.application.expiry_validator import ExpiryCandidateValidator
from pdf_agent.infrastructure.pdf_reader import PdfTextReader

FIXTURE_DIR = Path(__file__).resolve().parents[2]


class UnusedOCR:
    def extract(self, pdf_path):
        raise AssertionError("OCR should not be needed for a text-based PDF")


class UnusedLLM:
    def extract_expiry(self, pages):
        raise AssertionError("LLM should not be needed when the rule-based extractor succeeds")


def test_extracts_expiry_from_real_pdf():
    agent = ExpiryAgent(
        pdf_reader=PdfTextReader(),
        ocr=UnusedOCR(),
        llm=UnusedLLM(),
        validator=ExpiryCandidateValidator(),
        date_extractor=DateCandidateExtractor(),
    )

    result = agent.run(str(FIXTURE_DIR / "testing_pdf_1.pdf"))

    assert result.expiry_date == date(2028, 12, 31)
    assert result.evidence.extraction_method == "rule"
