import sys
from pdf_agent.application.expiry_validator import ExpiryCandidateValidator
from pdf_agent.application.expiry_service import (
    ExpiryExtractionService,
)
from pdf_agent.infrastructure.pdf_reader import PdfTextReader
from pdf_agent.infrastructure.ocr import TesseractOCR
from pdf_agent.infrastructure.llm import OllamaLLM


def main():

    if len(sys.argv) < 2:
        print("Usage: python -m pdf_agent.cli <pdf_path>")
        return

    pdf_path = sys.argv[1]
    validator = ExpiryCandidateValidator()

    service = ExpiryExtractionService(
        pdf_reader=PdfTextReader(),
        ocr=TesseractOCR(),
        llm=OllamaLLM(),
        validator=validator,
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