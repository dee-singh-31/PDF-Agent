from abc import ABC, abstractmethod

from pdf_agent.domain.models import DocumentPage, ExpiryCandidate


class CandidateExtractor(ABC):

    @abstractmethod
    def extract(
        self,
        page: DocumentPage,
    ) -> list[ExpiryCandidate]:
        pass