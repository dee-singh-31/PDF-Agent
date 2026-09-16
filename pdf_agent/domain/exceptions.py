class PDFAgentError(Exception):
    pass


class DocumentReadError(PDFAgentError):
    pass


class UnreadableDocumentError(PDFAgentError):
    pass
