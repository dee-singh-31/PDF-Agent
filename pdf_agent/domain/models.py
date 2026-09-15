from dataclasses import dataclass
from datetime import date


@dataclass
class ExpiryCandidate:
    expiry_date: date
    reasoning: str
    source_text: str


@dataclass
class ExtractionResult:
    expiry_date: date | None
    reasoning: str | None