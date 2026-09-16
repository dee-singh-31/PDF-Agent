from abc import ABC, abstractmethod

from pdf_agent.domain.models import DocumentPage, ExpiryCandidate


class LLM(ABC):

    @abstractmethod
    def extract_expiry(
        self,
        pages: list[DocumentPage],
    ) -> list[ExpiryCandidate]:
        pass