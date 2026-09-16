import logging

from pdf_agent.application.expiry_validator import ExpiryCandidateValidator
from pdf_agent.application.ports.candidate_extractor import CandidateExtractor
from pdf_agent.application.ports.llm import LLM
from pdf_agent.application.ports.ocr import OCR
from pdf_agent.application.ports.pdf_reader import PDFReader
from pdf_agent.domain.exceptions import UnreadableDocumentError
from pdf_agent.domain.models import (
    Evidence,
    ExpiryCandidate,
    ExtractionResult,
)

logger = logging.getLogger(__name__)


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
        logger.debug("Read %d page(s) via PDF text extraction", len(pages))

        if not any(page.text for page in pages):
            logger.info("No extractable text found; falling back to OCR")
            pages = self.ocr.extract(pdf_path)

        if not any(page.text for page in pages):
            raise UnreadableDocumentError(
                f"Could not extract readable text from PDF: {pdf_path}"
            )

        candidates = []

        for page in pages:
            candidates.extend(
                self.date_extractor.extract(page)
            )

        logger.debug("Rule-based extractor found %d candidate(s)", len(candidates))

        best_candidate = self.validator.select_best(candidates)

        if best_candidate is None:
            logger.info("No valid rule-based candidate; falling back to LLM")
            llm_candidates = self.llm.extract_expiry(pages)
            best_candidate = self.validator.select_best(llm_candidates)

        if best_candidate is None:
            logger.info("No valid expiry date found")
        else:
            logger.info(
                "Selected candidate via %s extraction (page %s)",
                best_candidate.extraction_method or "unknown",
                best_candidate.page_number,
            )

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