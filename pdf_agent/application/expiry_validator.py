from datetime import date

from pdf_agent.domain.models import ExpiryCandidate


class ExpiryCandidateValidator:
    def select_best(
        self,
        candidates: list[ExpiryCandidate],
    ) -> ExpiryCandidate | None:

        valid_candidates = [
            candidate
            for candidate in candidates
            if self._is_valid(candidate)
        ]

        if not valid_candidates:
            return None

        return self._rank(valid_candidates)[0]

    def _is_valid(self, candidate: ExpiryCandidate) -> bool:
        # An expiry date should not already be in the past.
        return candidate.expiry_date >= date.today()

    def _rank(
        self,
        candidates: list[ExpiryCandidate],
    ) -> list[ExpiryCandidate]:

        # For now, prefer candidates whose source text
        # explicitly contains "expiry".
        return sorted(
            candidates,
            key=lambda candidate: "expiry" not in candidate.source_text.lower(),
        )