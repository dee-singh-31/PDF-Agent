from pypdf import PdfReader

from pdf_agent.application.ports.pdf_reader import PDFReader
from pdf_agent.domain.models import DocumentPage


class PdfTextReader(PDFReader):

    def read(self, pdf_path: str) -> list[DocumentPage]:
        reader = PdfReader(pdf_path)

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