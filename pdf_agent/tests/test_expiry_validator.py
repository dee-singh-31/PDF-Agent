from datetime import date, timedelta

from pdf_agent.application.expiry_validator import ExpiryCandidateValidator
from pdf_agent.domain.models import ExpiryCandidate


def make_candidate(days_from_today: int, source_text: str = "") -> ExpiryCandidate:
    return ExpiryCandidate(
        expiry_date=date.today() + timedelta(days=days_from_today),
        reasoning="test",
        source_text=source_text,
    )


def test_select_best_returns_none_when_no_candidates():
    validator = ExpiryCandidateValidator()

    assert validator.select_best([]) is None


def test_select_best_filters_out_past_dates():
    validator = ExpiryCandidateValidator()
    expired = make_candidate(-10)
    future = make_candidate(10)

    result = validator.select_best([expired, future])

    assert result is future


def test_select_best_returns_none_when_all_expired():
    validator = ExpiryCandidateValidator()
    candidates = [make_candidate(-1), make_candidate(-100)]

    assert validator.select_best(candidates) is None


def test_select_best_prefers_candidate_mentioning_expiry():
    validator = ExpiryCandidateValidator()
    plain = make_candidate(10, source_text="Valid until 2099-01-01")
    explicit = make_candidate(10, source_text="Expiry: 2099-01-01")

    result = validator.select_best([plain, explicit])

    assert result is explicit
