from pdf_agent.application.expiry_validator import ExpiryCandidateValidator
from pdf_agent.application.ports.candidate_extractor import CandidateExtractor
from pdf_agent.application.ports.llm import LLM
from pdf_agent.application.ports.ocr import OCR
from pdf_agent.application.ports.pdf_reader import PDFReader
from pdf_agent.domain.models import (
    Evidence,
    ExpiryCandidate,
    ExtractionResult,
)


class ExpiryAgent:

    def __init__(
        self,
        pdf_reader: PDFReader,
        ocr: OCR,
        llm: LLM,
        validator: ExpiryCandidateValidator,
        date_extractor: CandidateExtractor,
    ):
        self.pdf_reader = pdf_reader
        self.ocr = ocr
        self.llm = llm
        self.validator = validator
        self.date_extractor = date_extractor

    def run(self, pdf_path: str) -> ExtractionResult:
        pages = self.pdf_reader.read(pdf_path)

        if not any(page.text for page in pages):
            pages = self.ocr.extract(pdf_path)

        if not any(page.text for page in pages):
            raise ValueError(
                "Could not extract readable text from PDF"
            )

        candidates = []

        for page in pages:
            candidates.extend(
                self.date_extractor.extract(page)
            )

        best_candidate = self.validator.select_best(candidates)

        if best_candidate is None:
            llm_candidates = self.llm.extract_expiry(pages)
            best_candidate = self.validator.select_best(llm_candidates)

        return self._to_result(best_candidate)

    def _to_result(
        self,
        candidate: ExpiryCandidate | None,
    ) -> ExtractionResult:

        if candidate is None:
            return ExtractionResult(
                expiry_date=None,
                reasoning="No valid expiry date was found",
            )

        return ExtractionResult(
            expiry_date=candidate.expiry_date,
            reasoning=candidate.reasoning,
            evidence=Evidence(
                page_number=candidate.page_number,
                source_text=candidate.source_text,
                extraction_method=candidate.extraction_method or "unknown",
                reasoning=candidate.reasoning,
            ),
        )