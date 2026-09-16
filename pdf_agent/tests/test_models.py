from datetime import date

from pdf_agent.domain.models import (
    DocumentPage,
    Evidence,
    ExpiryCandidate,
    ExtractionResult,
)


def test_document_page():
    page = DocumentPage(
        page_number=2,
        text="Expires: 2028-12-31",
    )

    assert page.page_number == 2
    assert page.text == "Expires: 2028-12-31"


def test_expiry_candidate():
    candidate = ExpiryCandidate(
        expiry_date=date(2028, 12, 31),
        reasoning="Found expiry date on page 2",
        source_text="Expires: 2028-12-31",
        page_number=2,
        extraction_method="rule",
    )

    assert candidate.expiry_date == date(2028, 12, 31)
    assert candidate.page_number == 2
    assert candidate.extraction_method == "rule"


def test_evidence():
    evidence = Evidence(
        page_number=2,
        source_text="Expires: 2028-12-31",
        extraction_method="rule",
        reasoning="Found expiry date on page 2",
    )

    assert evidence.page_number == 2
    assert evidence.source_text == "Expires: 2028-12-31"
    assert evidence.extraction_method == "rule"


def test_extraction_result_with_evidence():
    evidence = Evidence(
        page_number=2,
        source_text="Expires: 2028-12-31",
        extraction_method="rule",
        reasoning="Found expiry date on page 2",
    )

    result = ExtractionResult(
        expiry_date=date(2028, 12, 31),
        reasoning="Found expiry date on page 2",
        evidence=evidence,
    )

    assert result.expiry_date == date(2028, 12, 31)
    assert result.evidence is not None
    assert result.evidence.page_number == 2
    assert result.evidence.extraction_method == "rule"


def test_extraction_result_without_evidence():
    result = ExtractionResult(
        expiry_date=None,
        reasoning="No valid expiry date was found",
    )

    assert result.expiry_date is None
    assert result.evidence is None