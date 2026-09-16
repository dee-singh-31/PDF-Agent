import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    ollama_model: str = os.getenv("PDF_AGENT_OLLAMA_MODEL", "llama3.2")
    poppler_path: str | None = os.getenv("PDF_AGENT_POPPLER_PATH")
