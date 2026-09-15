import json
from datetime import date

import ollama

from pdf_agent.domain.models import ExpiryCandidate


class OllamaLLM:
    def __init__(self, model: str = "llama3.2"):
        self.model = model

    def extract_expiry(
        self,
        document_text: str,
    ) -> list[ExpiryCandidate]:

        prompt = f"""
You are an expert document analysis agent.

Analyze the following document text and identify all possible expiration dates.

Return ONLY a valid JSON object.
Do not use Markdown.
Do not include ```json.
Do not include any text before or after the JSON.

Required format:

{{
    "candidates": [
        {{
            "expiry_date": "YYYY-MM-DD",
            "reasoning": "A short sentence explaining why this could be the expiry date",
            "source_text": "The exact relevant text from the document"
        }}
    ]
}}

If no possible expiry date is found, return:

{{
    "candidates": []
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

        raw_response = response["message"]["content"]

        return self._parse_response(raw_response)

    def _parse_response(
        self,
        raw_response: str,
    ) -> list[ExpiryCandidate]:

        try:
            data = json.loads(raw_response)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"LLM returned invalid JSON: {raw_response}"
            ) from exc

        candidates = []

        for item in data.get("candidates", []):
            expiry_date = item.get("expiry_date")
            reasoning = item.get("reasoning", "")
            source_text = item.get("source_text", "")

            if not expiry_date:
                continue

            try:
                parsed_date = date.fromisoformat(expiry_date)
            except ValueError as exc:
                raise ValueError(
                    f"LLM returned invalid expiry date: {expiry_date}"
                ) from exc

            candidates.append(
                ExpiryCandidate(
                    expiry_date=parsed_date,
                    reasoning=reasoning,
                    source_text=source_text,
                )
            )

        return candidates