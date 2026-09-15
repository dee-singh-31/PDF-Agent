from pdf_agent.domain.models import ExtractionResult
from pdf_agent.application.expiry_validator import ExpiryCandidateValidator


class ExpiryExtractionService:
    def __init__(self, pdf_reader, ocr, llm, validator):
        self.pdf_reader = pdf_reader
        self.ocr = ocr
        self.llm = llm
        self.validator = validator

    def extract(self, pdf_path: str) -> ExtractionResult:
        text = self.pdf_reader.read(pdf_path)

        if not text:
            text = self.ocr.extract(pdf_path)

        if not text:
            raise ValueError("Could not extract readable text from PDF")

        candidates = self.llm.extract_expiry(text)

        if not candidates:
            return ExtractionResult(
                expiry_date=None,
                reasoning="No expiry date was found",
            )

        best_candidate = self.validator.select_best(candidates)

        if best_candidate is None:
            return ExtractionResult(
                expiry_date=None,
                reasoning="No valid expiry date was found",
            )

        return ExtractionResult(
            expiry_date=best_candidate.expiry_date,
            reasoning=best_candidate.reasoning,
        )