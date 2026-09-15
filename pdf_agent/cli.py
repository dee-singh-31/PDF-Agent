import sys

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

    service = ExpiryExtractionService(
        pdf_reader=PdfTextReader(),
        ocr=TesseractOCR(),
        llm=OllamaLLM(),
    )

    result = service.extract(pdf_path)

    print(result)


if __name__ == "__main__":
    main()