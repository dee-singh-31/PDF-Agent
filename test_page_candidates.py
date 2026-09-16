from pdf_agent.application.ports.pdf_reader import PdfTextReader
from pdf_agent.application.date_candidate_extractor import DateCandidateExtractor


reader = PdfTextReader()
extractor = DateCandidateExtractor()

pages = reader.read("testing_pdf_1.pdf")

for page in pages:
    candidates = extractor.extract(page)

    for candidate in candidates:
        print(candidate)