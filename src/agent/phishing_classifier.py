import logging
import os
from typing import Any, Dict

from openai import OpenAI

logger = logging.getLogger(__name__)


class PhishingClassifier:
    def __init__(self, api_key: str = None, model: str = "gpt-4.1-mini"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY must be set in the environment")

        os.environ["OPENAI_API_KEY"] = self.api_key
        self.client = OpenAI(api_key=self.api_key)
        self.model = model

    def classify(self, message: Dict[str, Any]) -> Dict[str, Any]:
        sender = message.get("sender", "Unknown sender")
        subject = message.get("subject", "No subject")
        body = message.get("body", "")

        prompt = (
            "You are a phishing classification assistant. "
            "Classify the following email content as either PHISHING or SAFE. "
            "Return your answer with a single label on the first line, either PHISHING or SAFE, "
            "and then provide a short rationale.\n\n"
            f"Sender: {sender}\n"
            f"Subject: {subject}\n"
            f"Body: {body}\n"
            "\nRespond with exactly one label on the first line, followed by a short explanation."
        )

        response = self.client.responses.create(
            model=self.model,
            input=prompt,
            max_output_tokens=200,
        )

        text = self._extract_response_text(response)
        classification = self._parse_classification(text)
        reason = text.strip() or "OpenAI classification returned no text."

        return {
            "is_phishing": classification == "PHISHING",
            "classification": classification,
            "reason": reason,
        }

    def _extract_response_text(self, response: Any) -> str:
        if hasattr(response, "output_text") and response.output_text:
            return response.output_text

        raw_output = getattr(response, "output", None)
        if isinstance(raw_output, list):
            fragments = []
            for item in raw_output:
                if isinstance(item, dict):
                    content = item.get("content")
                    if isinstance(content, list):
                        for block in content:
                            if isinstance(block, dict) and block.get("type") == "output_text":
                                fragments.append(block.get("text", ""))
            return "\n".join(fragments)

        return str(response)

    def _parse_classification(self, text: str) -> str:
        normalized = text.strip().upper()
        if normalized.startswith("PHISHING"):
            return "PHISHING"
        if normalized.startswith("SAFE"):
            return "SAFE"
        if "PHISHING" in normalized and "SAFE" not in normalized:
            return "PHISHING"
        return "SAFE"
