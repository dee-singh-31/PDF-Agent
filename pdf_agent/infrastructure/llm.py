from typing import Protocol


class LLMClient(Protocol):

    def extract_expiry(self, document_text: str) -> str:
        ...
import ollama


class OllamaLLM:

    def __init__(self, model: str = "llama3.2"):
        self.model = model

    def extract_expiry(self, document_text: str) -> str:

        prompt = f"""
You are an expert document analysis agent.

Analyze the following text layout and extract the expiration date.

Respond ONLY with a raw JSON object matching this schema:

{{
    "expiry_date": "YYYY-MM-DD or null if not found",
    "reasoning": "A short sentence explaining where it was found"
}}

Document Text:

{document_text}
"""

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response["message"]["content"]