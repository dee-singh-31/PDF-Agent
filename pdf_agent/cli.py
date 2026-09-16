import sys

from pdf_agent.application.agent import ExpiryAgent
from pdf_agent.application.date_candidate_extractor import DateCandidateExtractor
from pdf_agent.application.expiry_validator import ExpiryCandidateValidator
from pdf_agent.config import Settings
from pdf_agent.infrastructure.llm import OllamaLLM
from pdf_agent.infrastructure.ocr import TesseractOCR
from pdf_agent.infrastructure.pdf_reader import PdfTextReader


def build_agent(settings: Settings) -> ExpiryAgent:
    return ExpiryAgent(
        pdf_reader=PdfTextReader(),
        ocr=TesseractOCR(poppler_path=settings.poppler_path),
        llm=OllamaLLM(model=settings.ollama_model),
        validator=ExpiryCandidateValidator(),
        date_extractor=DateCandidateExtractor(),
    )


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 -m pdf_agent.cli <pdf_path>")
        sys.exit(1)

    pdf_path = sys.argv[1]

    agent = build_agent(Settings())

    result = agent.run(pdf_path)

    if result.expiry_date:
        print(f"Expiry Date: {result.expiry_date}")
    else:
        print("Expiry Date: Not found")

    if result.reasoning:
        print(f"Reasoning: {result.reasoning}")


if __name__ == "__main__":
    main()