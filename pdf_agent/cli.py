import argparse
import dataclasses
import logging
import sys

from pdf_agent.application.agent import ExpiryAgent
from pdf_agent.application.date_candidate_extractor import DateCandidateExtractor
from pdf_agent.application.expiry_validator import ExpiryCandidateValidator
from pdf_agent.config import Settings
from pdf_agent.domain.exceptions import PDFAgentError
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


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract the expiry date from a PDF document."
    )
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument(
        "--model",
        default=None,
        help="Ollama model to use for the LLM fallback "
        "(default: $PDF_AGENT_OLLAMA_MODEL or llama3.2)",
    )
    parser.add_argument(
        "--poppler-path",
        default=None,
        help="Path to the poppler binaries used for OCR "
        "(default: $PDF_AGENT_POPPLER_PATH)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Log each pipeline stage (text extraction, OCR, rule-based "
        "matching, LLM fallback) to stderr",
    )
    return parser.parse_args(argv)


def build_settings(args: argparse.Namespace) -> Settings:
    settings = Settings()

    overrides = {}

    if args.model:
        overrides["ollama_model"] = args.model

    if args.poppler_path:
        overrides["poppler_path"] = args.poppler_path

    return dataclasses.replace(settings, **overrides)


def main():
    args = parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.WARNING,
        format="%(levelname)s %(name)s: %(message)s",
    )

    agent = build_agent(build_settings(args))

    try:
        result = agent.run(args.pdf_path)
    except PDFAgentError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    if result.expiry_date:
        print(f"Expiry Date: {result.expiry_date}")
    else:
        print("Expiry Date: Not found")

    if result.reasoning:
        print(f"Reasoning: {result.reasoning}")


if __name__ == "__main__":
    main()
