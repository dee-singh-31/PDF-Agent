from abc import ABC, abstractmethod

from pdf_agent.domain.models import DocumentPage


class OCR(ABC):

    @abstractmethod
    def extract(self, pdf_path: str) -> list[DocumentPage]:
        pass