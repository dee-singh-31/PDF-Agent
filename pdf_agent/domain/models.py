from dataclasses import dataclass
from datetime import date


@dataclass
class ExpiryExtraction:
    expiry_date: date | None
    reasoning: str | None
    confidence: float
    source_page: int | None
    raw_value: str | None
    method: str