from __future__ import annotations

import asyncio
import json
from typing import Any

import httpx
from pydantic import BaseModel, ValidationError

from app.core.config import settings
from app.core.errors import ExternalServiceError, ValidationFailure
from app.core.logging import Timer, get_logger

log = get_logger(__name__)


class NimClient:
    def __init__(self) -> None:
        self._base = settings.nim_base_url.rstrip("/")
        self._timeout = settings.nim_timeout_s
        self._max_retries = settings.nim_max_retries

    async def chat_json(self, *, system: str, user: str, schema: type[BaseModel], request_id: str | None) -> BaseModel:
        url = f"{self._base}/chat/completions"
        headers = {"Authorization": f"Bearer {settings.nim_api_key}", "Content-Type": "application/json"}
        payload = {
            "model": settings.nim_model,
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
            "temperature": 0.2,
            "max_tokens": 512,
        }

        last_err: Exception | None = None
        for attempt in range(self._max_retries + 1):
            t = Timer()
            try:
                async with httpx.AsyncClient(timeout=self._timeout) as client:
                    resp = await client.post(url, headers=headers, json=payload)
                log.info(
                    "nim_call",
                    extra={
                        "request_id": request_id,
                        "attempt": attempt,
                        "status_code": resp.status_code,
                        "latency_ms": t.ms(),
                        "model": settings.nim_model,
                    },
                )
                if resp.status_code >= 400:
                    raise ExternalServiceError(f"NIM status={resp.status_code}")

                data = resp.json()
                content = data["choices"][0]["message"]["content"]
                return self._parse_validate(content, schema)

            except (httpx.HTTPError, KeyError, ExternalServiceError, ValidationFailure) as e:
                last_err = e
                if attempt < self._max_retries:
                    await asyncio.sleep(0.5 * (attempt + 1))
                    continue
                break

        raise ExternalServiceError(str(last_err) if last_err else "NIM call failed")

    def _parse_validate(self, content: str, schema: type[BaseModel]) -> BaseModel:
        try:
            raw = json.loads(content)
        except json.JSONDecodeError:
            raw = _extract_json_object(content)
            if raw is None:
                raise ValidationFailure("Model did not return valid JSON")

        try:
            return schema.model_validate(raw)
        except ValidationError as e:
            raise ValidationFailure(f"Schema validation failed: {e.errors()[:1]}")


def _extract_json_object(text: str) -> dict[str, Any] | None:
    s = text.find("{")
    e = text.rfind("}")
    if s == -1 or e == -1 or e <= s:
        return None
    try:
        return json.loads(text[s : e + 1])
    except json.JSONDecodeError:
        return None
