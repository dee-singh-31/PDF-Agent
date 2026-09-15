class ExpiryExtractionService:

    def __init__(
        self,
        pdf_reader,
        ocr,
        llm,
    ):
        self.pdf_reader = pdf_reader
        self.ocr = ocr
        self.llm = llm

    def extract(self, pdf_path: str):

        text = self.pdf_reader.read(pdf_path)

        if not text:
            text = self.ocr.extract(pdf_path)

        if not text:
            raise ValueError(
                "Could not extract readable text from PDF"
            )

        return self.llm.extract_expiry(text)