from pypdf import PdfReader


class PdfTextReader:

    def read(self, pdf_path: str) -> str:
        reader = PdfReader(pdf_path)

        text_parts = []

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text_parts.append(page_text)

        return "\n".join(text_parts).strip()