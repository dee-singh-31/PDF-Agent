from pdf_agent.application.ports.candidate_extractor import CandidateExtractor
from pdf_agent.application.ports.llm import LLM
from pdf_agent.application.ports.ocr import OCR
from pdf_agent.application.ports.pdf_reader import PDFReader
from pdf_agent.application.expiry_validator import ExpiryCandidateValidator
from pdf_agent.domain.models import ExtractionResult


class ExpiryExtractionService:

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

    def extract(self, pdf_path: str) -> ExtractionResult:
        pages = self.pdf_reader.read(pdf_path)

        has_text = any(page.text for page in pages)

        if not has_text:
            pages = self.ocr.extract(pdf_path)

        has_text = any(page.text for page in pages)

        if not has_text:
            raise ValueError(
                "Could not extract readable text from PDF"
            )

        candidates = []

        for page in pages:
            page_candidates = self.date_extractor.extract(page)
            candidates.extend(page_candidates)

        if not candidates:
            candidates = self.llm.extract_expiry(pages)

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