from pdf2image import convert_from_path
import pytesseract


class TesseractOCR:

    def extract(self, pdf_path: str) -> str:
        pages = convert_from_path(
            pdf_path,
            first_page=1,
            last_page=1,
            poppler_path="/opt/homebrew/bin",
        )

        if not pages:
            return ""

        return pytesseract.image_to_string(pages[0]).strip()