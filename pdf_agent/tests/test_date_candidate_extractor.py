from datetime import date

from pdf_agent.application.date_candidate_extractor import DateCandidateExtractor
from pdf_agent.domain.models import DocumentPage


def test_extracts_expiry_date_pattern():
    extractor = DateCandidateExtractor()
    page = DocumentPage(page_number=1, text="Expiry Date: 2028-12-31")

    candidates = extractor.extract(page)

    assert len(candidates) == 1
    assert candidates[0].expiry_date == date(2028, 12, 31)
    assert candidates[0].page_number == 1
    assert candidates[0].extraction_method == "rule"


def test_extracts_valid_until_pattern():
    extractor = DateCandidateExtractor()
    page = DocumentPage(page_number=3, text="This license is valid until 2030-06-15.")

    candidates = extractor.extract(page)

    assert len(candidates) == 1
    assert candidates[0].expiry_date == date(2030, 6, 15)


def test_ignores_unrelated_dates():
    extractor = DateCandidateExtractor()
    page = DocumentPage(page_number=1, text="Issue Date: 2020-01-01, no expiry mentioned.")

    candidates = extractor.extract(page)

    assert candidates == []


def test_returns_empty_list_for_no_matches():
    extractor = DateCandidateExtractor()
    page = DocumentPage(page_number=1, text="Nothing relevant here.")

    assert extractor.extract(page) == []
