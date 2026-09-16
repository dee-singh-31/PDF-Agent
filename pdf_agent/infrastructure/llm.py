import json
from datetime import date

import ollama

from pdf_agent.application.ports.llm import LLM
from pdf_agent.domain.models import DocumentPage, ExpiryCandidate


class OllamaLLM(LLM):

    def __init__(self, model: str = "llama3.2"):
        self.model = model

    def extract_expiry(
        self,
        pages: list[DocumentPage],
    ) -> list[ExpiryCandidate]:

        document_text = "\n\n".join(
            f"--- Page {page.page_number} ---\n{page.text}"
            for page in pages
        )

        prompt = f"""
You are an expert document analysis agent.

Analyze the following document and identify all possible expiration dates.

Return ONLY valid JSON.

Do NOT summarize the document.
Do NOT explain your answer outside the JSON.
Do NOT return Markdown.
Do NOT use ```json.

Required format:

{{
    "candidates": [
        {{
            "expiry_date": "YYYY-MM-DD",
            "reasoning": "A short sentence explaining why this could be the expiry date",
            "source_text": "The exact relevant text from the document",
            "page_number": 2
        }}
    ]
}}

If no possible expiry date is found, return exactly:

{{
    "candidates": []
}}

Document:

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
            format="json",
        )

        raw_response = response["message"]["content"].strip()

        return self._parse_response(raw_response)

    def _parse_response(
        self,
        raw_response: str,
    ) -> list[ExpiryCandidate]:

        try:
            data = json.loads(raw_response)
        except json.JSONDecodeError as exc:
            raise ValueError(
                "LLM returned invalid JSON. "
                f"Raw response: {raw_response}"
            ) from exc

        if not isinstance(data, dict):
            raise ValueError(
                "LLM response must be a JSON object"
            )

        candidates = []

        for item in data.get("candidates", []):
            expiry_date = item.get("expiry_date")
            reasoning = item.get("reasoning", "")
            source_text = item.get("source_text", "")
            page_number = item.get("page_number")

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
                    page_number=page_number,
                )
            )

        return candidates