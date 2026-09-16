from datetime import date, timedelta

import pytest

from pdf_agent.application.agent import ExpiryAgent
from pdf_agent.application.date_candidate_extractor import DateCandidateExtractor
from pdf_agent.application.expiry_validator import ExpiryCandidateValidator
from pdf_agent.domain.models import DocumentPage, ExpiryCandidate

FUTURE = date.today() + timedelta(days=30)
PAST = date.today() - timedelta(days=30)


class FakePdfReader:
    def __init__(self, pages):
        self._pages = pages

    def read(self, pdf_path):
        return self._pages


class FakeOCR:
    def __init__(self, pages=None):
        self._pages = pages or []

    def extract(self, pdf_path):
        return self._pages


class FakeLLM:
    def __init__(self, candidates=None):
        self._candidates = candidates or []
        self.called = False

    def extract_expiry(self, pages):
        self.called = True
        return self._candidates


def build_agent(pdf_reader, ocr=None, llm=None):
    return ExpiryAgent(
        pdf_reader=pdf_reader,
        ocr=ocr or FakeOCR(),
        llm=llm or FakeLLM(),
        validator=ExpiryCandidateValidator(),
        date_extractor=DateCandidateExtractor(),
    )


def test_agent_uses_rule_based_candidate_when_valid():
    pages = [DocumentPage(page_number=1, text=f"Expiry Date: {FUTURE.isoformat()}")]
    llm = FakeLLM()
    agent = build_agent(FakePdfReader(pages), llm=llm)

    result = agent.run("doc.pdf")

    assert result.expiry_date == FUTURE
    assert result.evidence.extraction_method == "rule"
    assert llm.called is False


def test_agent_falls_back_to_llm_when_rule_based_finds_nothing():
    pages = [DocumentPage(page_number=1, text="No dates here.")]
    llm_candidate = ExpiryCandidate(
        expiry_date=FUTURE,
        reasoning="LLM found it",
        source_text="expires soon",
        page_number=1,
        extraction_method="llm",
    )
    llm = FakeLLM([llm_candidate])
    agent = build_agent(FakePdfReader(pages), llm=llm)

    result = agent.run("doc.pdf")

    assert result.expiry_date == FUTURE
    assert result.evidence.extraction_method == "llm"
    assert llm.called is True


def test_agent_falls_back_to_llm_when_all_rule_candidates_are_expired():
    pages = [DocumentPage(page_number=1, text=f"Expiry Date: {PAST.isoformat()}")]
    llm_candidate = ExpiryCandidate(
        expiry_date=FUTURE,
        reasoning="LLM found the real expiry",
        source_text="expires soon",
        page_number=1,
        extraction_method="llm",
    )
    llm = FakeLLM([llm_candidate])
    agent = build_agent(FakePdfReader(pages), llm=llm)

    result = agent.run("doc.pdf")

    assert result.expiry_date == FUTURE
    assert llm.called is True


def test_agent_returns_none_when_nothing_found_anywhere():
    pages = [DocumentPage(page_number=1, text="No dates here.")]
    agent = build_agent(FakePdfReader(pages), llm=FakeLLM([]))

    result = agent.run("doc.pdf")

    assert result.expiry_date is None
    assert result.evidence is None


def test_agent_falls_back_to_ocr_when_pdf_has_no_text():
    empty_pages = [DocumentPage(page_number=1, text="")]
    ocr_pages = [DocumentPage(page_number=1, text=f"Expiry Date: {FUTURE.isoformat()}")]
    agent = build_agent(
        FakePdfReader(empty_pages),
        ocr=FakeOCR(ocr_pages),
        llm=FakeLLM(),
    )

    result = agent.run("scanned.pdf")

    assert result.expiry_date == FUTURE


def test_agent_raises_when_no_text_from_pdf_or_ocr():
    empty_pages = [DocumentPage(page_number=1, text="")]
    agent = build_agent(FakePdfReader(empty_pages), ocr=FakeOCR([]))

    with pytest.raises(ValueError):
        agent.run("blank.pdf")
