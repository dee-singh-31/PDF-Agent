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
    extraction_method: str | None = None


@dataclass
class Evidence:
    page_number: int | None
    source_text: str
    extraction_method: str
    reasoning: str


@dataclass
class ExtractionResult:
    expiry_date: date | None
    reasoning: str | None
    evidence: Evidence | None = None