from pdf2image import convert_from_path
import pytesseract

from pdf_agent.application.ports.ocr import OCR
from pdf_agent.domain.exceptions import DocumentReadError
from pdf_agent.domain.models import DocumentPage


class TesseractOCR(OCR):

    def __init__(self, poppler_path: str | None = None):
        self.poppler_path = poppler_path

    def extract(self, pdf_path: str) -> list[DocumentPage]:
        kwargs = {}

        if self.poppler_path:
            kwargs["poppler_path"] = self.poppler_path

        try:
            images = convert_from_path(
                pdf_path,
                **kwargs,
            )
        except Exception as exc:
            raise DocumentReadError(
                f"Could not rasterize PDF for OCR: {pdf_path}"
            ) from exc

        pages = []

        for page_number, image in enumerate(images, start=1):
            text = pytesseract.image_to_string(image).strip()

            pages.append(
                DocumentPage(
                    page_number=page_number,
                    text=text,
                )
            )

        return pages