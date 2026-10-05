import json
import logging
import re
from typing import Any, Dict, Optional
import httpx

from app.config import settings

logger = logging.getLogger("ai_parallel_universe.llm")


class LLMService:
    """
    Centralized LLM service supporting both live API provider calls and dynamic mock mode.
    """

    def __init__(self):
        self.api_key = settings.LLM_API_KEY or settings.OPENAI_API_KEY
        self.model = settings.LLM_MODEL or "gpt-4o-mini"
        self.base_url = (settings.LLM_BASE_URL or "https://api.openai.com/v1").rstrip("/")
        self.mock_mode = settings.LLM_MOCK_MODE or not bool(self.api_key)

    async def generate_json(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """
        Sends a request to the LLM expecting a structured JSON object response.
        If in mock mode or API key is missing, returns None so caller can fallback to dynamic mock generator.
        """
        if self.mock_mode or not self.api_key:
            logger.info("LLM is operating in MOCK MODE.")
            return None

        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt + "\nReturn ONLY valid JSON format. Do not add conversational text or markdown code fences outside JSON."},
                {"role": "user", "content": user_prompt},
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.3,
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
                content = data["choices"][0]["message"]["content"]

                # Clean markdown code blocks if present
                content_clean = re.sub(r"^```(json)?\s*", "", content.strip(), flags=re.MULTILINE)
                content_clean = re.sub(r"\s*```$", "", content_clean, flags=re.MULTILINE)

                return json.loads(content_clean)
        except Exception as e:
            logger.warning(f"LLM API call failed: {e}. Falling back to dynamic mock implementation.")
            return None


llm_service = LLMService()
