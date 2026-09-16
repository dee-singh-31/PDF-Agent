from abc import ABC, abstractmethod

from pdf_agent.domain.models import DocumentPage


class PDFReader(ABC):

    @abstractmethod
    def read(self, pdf_path: str) -> list[DocumentPage]:
        pass