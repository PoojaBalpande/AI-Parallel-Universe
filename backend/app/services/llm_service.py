import asyncio
import json
import logging
import re
from typing import Any, Dict, Optional

import httpx

from app.config import settings


logger = logging.getLogger("ai_parallel_universe.llm")


class LLMServiceError(Exception):
    """Raised when an error occurs during LLM service execution in live mode."""

    pass


class LLMService:
    """
    Centralized LLM service supporting both live API provider calls
    and dynamic mock mode.
    """

    @property
    def is_mock_mode(self) -> bool:
        return bool(settings.LLM_MOCK_MODE)

    @property
    def api_key(self) -> Optional[str]:
        return settings.LLM_API_KEY or settings.OPENAI_API_KEY

    @property
    def model(self) -> str:
        return settings.LLM_MODEL or "gpt-4o-mini"

    @property
    def base_url(self) -> str:
        return (
            settings.LLM_BASE_URL or "https://api.openai.com/v1"
        ).rstrip("/")

    async def generate_json(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Sends a request to the LLM expecting a structured JSON object.

        Mock mode:
            Returns None so the calling service can use its explicit
            mock implementation.

        Live mode:
            Returns the real LLM JSON response.

            Retries temporary failures such as:
            - HTTP 429 Too Many Requests
            - HTTP 500 Internal Server Error
            - HTTP 502 Bad Gateway
            - HTTP 503 Service Unavailable
            - HTTP 504 Gateway Timeout
            - transient network errors

            Permanent errors are raised immediately.
        """

        # ---------------------------------------------------------
        # MOCK MODE
        # ---------------------------------------------------------
        if self.is_mock_mode:
            logger.info("LLM is operating in MOCK MODE.")
            return None

        # ---------------------------------------------------------
        # API KEY VALIDATION
        # ---------------------------------------------------------
        if not self.api_key:
            logger.error(
                "LLM API key is missing while LLM_MOCK_MODE=false."
            )

            raise LLMServiceError(
                "LLM API key is missing or not configured "
                "for live LLM mode."
            )

        # ---------------------------------------------------------
        # API CONFIGURATION
        # ---------------------------------------------------------
        url = f"{self.base_url}/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        system_prompt
                        + "\nReturn ONLY valid JSON format. "
                        "Do not add conversational text or markdown "
                        "code fences outside JSON."
                    ),
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.3,
        }

        # Maximum number of retries after the initial request.
        # Total attempts = 3.
        max_retries = 2

        # ---------------------------------------------------------
        # REQUEST + RETRY LOOP
        # ---------------------------------------------------------
        for attempt in range(max_retries + 1):

            try:
                async with httpx.AsyncClient(
                    timeout=30.0
                ) as client:

                    response = await client.post(
                        url,
                        headers=headers,
                        json=payload,
                    )

                # -------------------------------------------------
                # TEMPORARY HTTP ERRORS
                # -------------------------------------------------
                if response.status_code in {
                    429,
                    500,
                    502,
                    503,
                    504,
                }:

                    if attempt < max_retries:

                        # Respect Retry-After if the provider sends it.
                        retry_after = response.headers.get(
                            "retry-after"
                        )

                        if retry_after:
                            try:
                                delay = float(retry_after)
                            except ValueError:
                                delay = 2 ** (attempt + 1)
                        else:
                            # Exponential backoff:
                            # attempt 0 -> 2 sec
                            # attempt 1 -> 4 sec
                            delay = 2 ** (attempt + 1)

                        logger.warning(
                            "Temporary LLM error %s. "
                            "Retrying in %.1f seconds "
                            "(attempt %d/%d).",
                            response.status_code,
                            delay,
                            attempt + 1,
                            max_retries,
                        )

                        await asyncio.sleep(delay)
                        continue

                    # Retries exhausted
                    logger.error(
                        "LLM request failed after %d retries: "
                        "HTTP %s",
                        max_retries,
                        response.status_code,
                    )

                # -------------------------------------------------
                # RAISE FOR OTHER HTTP ERRORS
                # -------------------------------------------------
                response.raise_for_status()

                # -------------------------------------------------
                # PARSE RESPONSE
                # -------------------------------------------------
                data = response.json()

                content = data["choices"][0]["message"]["content"]

                # -------------------------------------------------
                # CLEAN MARKDOWN CODE FENCES
                # -------------------------------------------------
                content_clean = re.sub(
                    r"^```(json)?\s*",
                    "",
                    content.strip(),
                    flags=re.MULTILINE,
                )

                content_clean = re.sub(
                    r"\s*```$",
                    "",
                    content_clean,
                    flags=re.MULTILINE,
                )

                # -------------------------------------------------
                # PARSE JSON CONTENT
                # -------------------------------------------------
                return json.loads(content_clean)

            # -----------------------------------------------------
            # NETWORK / TIMEOUT ERRORS
            # -----------------------------------------------------
            except httpx.RequestError as e:

                if attempt < max_retries:

                    delay = 2 ** (attempt + 1)

                    logger.warning(
                        "Transient LLM network error: %s. "
                        "Retrying in %.1f seconds "
                        "(attempt %d/%d).",
                        e,
                        delay,
                        attempt + 1,
                        max_retries,
                    )

                    await asyncio.sleep(delay)
                    continue

                logger.error(
                    "LLM network request failed after retries: %s",
                    e,
                )

                raise LLMServiceError(
                    f"LLM service call failed: {e}"
                ) from e

            # -----------------------------------------------------
            # HTTP STATUS ERRORS
            # -----------------------------------------------------
            except httpx.HTTPStatusError as e:

                logger.error(
                    "LLM API returned HTTP %s: %s",
                    e.response.status_code,
                    e,
                )

                raise LLMServiceError(
                    f"LLM service call failed: {e}"
                ) from e

            # -----------------------------------------------------
            # INVALID RESPONSE / JSON ERRORS
            # -----------------------------------------------------
            except (
                KeyError,
                TypeError,
                json.JSONDecodeError,
            ) as e:

                logger.error(
                    "Invalid JSON response from LLM: %s",
                    e,
                )

                raise LLMServiceError(
                    f"Invalid LLM response format: {e}"
                ) from e

            # -----------------------------------------------------
            # UNEXPECTED ERRORS
            # -----------------------------------------------------
            except Exception as e:

                logger.error(
                    "Unexpected LLM API error: %s",
                    e,
                )

                raise LLMServiceError(
                    f"LLM service call failed: {e}"
                ) from e

        # ---------------------------------------------------------
        # FALLBACK IF RETRY LOOP EXITS UNEXPECTEDLY
        # ---------------------------------------------------------
        raise LLMServiceError(
            "LLM service call failed after retries."
        )


llm_service = LLMService()