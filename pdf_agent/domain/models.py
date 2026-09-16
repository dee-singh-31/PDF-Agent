from dataclasses import dataclass
from datetime import date


@dataclass
class DocumentPage:
    page_number: int
    text: str


@dataclass
class ExpiryCandidate:
    expiry_date: date
    reasoning: str
    source_text: str
    page_number: int | None = None


@dataclass
class ExtractionResult:
    expiry_date: date | None
    reasoning: str | None