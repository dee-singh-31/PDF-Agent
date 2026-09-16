from pypdf import PdfReader

from pdf_agent.application.ports.pdf_reader import PDFReader
from pdf_agent.domain.exceptions import DocumentReadError
from pdf_agent.domain.models import DocumentPage


class PdfTextReader(PDFReader):

    def read(self, pdf_path: str) -> list[DocumentPage]:
        try:
            reader = PdfReader(pdf_path)
        except Exception as exc:
            raise DocumentReadError(
                f"Could not read PDF file: {pdf_path}"
            ) from exc

        pages = []

        for page_number, page in enumerate(reader.pages, start=1):
            page_text = page.extract_text() or ""

            pages.append(
                DocumentPage(
                    page_number=page_number,
                    text=page_text.strip(),
                )
            )

        return pages