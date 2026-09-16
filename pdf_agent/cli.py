import sys

from pdf_agent.application.date_candidate_extractor import DateCandidateExtractor
from pdf_agent.application.expiry_service import ExpiryExtractionService
from pdf_agent.application.expiry_validator import ExpiryCandidateValidator
from pdf_agent.application.ports.llm import OllamaLLM
from pdf_agent.application.ports.ocr import TesseractOCR
from pdf_agent.application.ports.pdf_reader import PdfTextReader


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 -m pdf_agent.cli <pdf_path>")
        sys.exit(1)

    pdf_path = sys.argv[1]

    pdf_reader = PdfTextReader()
    ocr = TesseractOCR()
    llm = OllamaLLM()
    validator = ExpiryCandidateValidator()
    date_extractor = DateCandidateExtractor()

    service = ExpiryExtractionService(
        pdf_reader=pdf_reader,
        ocr=ocr,
        llm=llm,
        validator=validator,
        date_extractor=date_extractor,
    )

    result = service.extract(pdf_path)

    if result.expiry_date:
        print(f"Expiry Date: {result.expiry_date}")
    else:
        print("Expiry Date: Not found")

    if result.reasoning:
        print(f"Reasoning: {result.reasoning}")


if __name__ == "__main__":
    main()