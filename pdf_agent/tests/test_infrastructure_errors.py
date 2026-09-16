from unittest.mock import patch

import pytest

from pdf_agent.domain.exceptions import DocumentReadError
from pdf_agent.infrastructure.ocr import TesseractOCR
from pdf_agent.infrastructure.pdf_reader import PdfTextReader


def test_pdf_reader_wraps_library_failures():
    reader = PdfTextReader()

    with pytest.raises(DocumentReadError):
        reader.read("does-not-exist.pdf")


def test_ocr_wraps_library_failures():
    ocr = TesseractOCR()

    with patch(
        "pdf_agent.infrastructure.ocr.convert_from_path",
        side_effect=RuntimeError("poppler not found"),
    ):
        with pytest.raises(DocumentReadError):
            ocr.extract("does-not-exist.pdf")
