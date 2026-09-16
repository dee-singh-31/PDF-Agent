import re
from datetime import datetime

from pdf_agent.domain.models import DocumentPage, ExpiryCandidate
from pdf_agent.application.ports.candidate_extractor import CandidateExtractor


class DateCandidateExtractor(CandidateExtractor):
    EXPIRY_PATTERNS = [
        r"expiry\s*date\s*[:\-]?\s*(\d{4}-\d{2}-\d{2})",
        r"expiration\s*date\s*[:\-]?\s*(\d{4}-\d{2}-\d{2})",
        r"expires?\s*[:\-]?\s*(\d{4}-\d{2}-\d{2})",
        r"valid\s*(?:until|through)\s*[:\-]?\s*(\d{4}-\d{2}-\d{2})",
    ]

    def extract(
        self,
        page: DocumentPage,
    ) -> list[ExpiryCandidate]:

        candidates = []

        for pattern in self.EXPIRY_PATTERNS:
            for match in re.finditer(
                pattern,
                page.text,
                re.IGNORECASE,
            ):
                date_string = match.group(1)

                try:
                    expiry_date = datetime.strptime(
                        date_string,
                        "%Y-%m-%d",
                    ).date()
                except ValueError:
                    continue

                candidates.append(
                    ExpiryCandidate(
                        expiry_date=expiry_date,
                        reasoning=(
                            f"Found using a rule-based expiry-date "
                            f"pattern on page {page.page_number}"
                        ),
                        source_text=match.group(0),
                        page_number=page.page_number,
                    )
                )

        return candidates