from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from pydantic import BaseModel

from app.core.logging import Timer, get_logger
from app.schemas.enrich import EnrichRequest, EnrichResponse
from app.services.nim_client import NimClient
from app.services.prompts import ENRICH_SYSTEM_PROMPT, ENRICH_USER_PROMPT
from app.services.supabase_repo import SupabaseRepo

log = get_logger(__name__)


class EnrichOut(BaseModel):
    summary: str
    category: str
    priority: str
    tags: list[str]
    action_items: list[str]


nim = NimClient()
repo = SupabaseRepo()


async def enrich_text(req: EnrichRequest, *, request_id: str | None) -> EnrichResponse:
    rid = request_id or str(uuid4())
    t = Timer()

    out = await nim.chat_json(
        system=ENRICH_SYSTEM_PROMPT,
        user=ENRICH_USER_PROMPT.format(text=req.text),
        schema=EnrichOut,
        request_id=rid,
    )

    latency_ms = t.ms()
    log.info("enrich_ok", extra={"request_id": rid, "latency_ms": latency_ms})

    resp = EnrichResponse(
        summary=out.summary,
        category=out.category,
        priority=out.priority,
        tags=out.tags,
        action_items=out.action_items,
        model=settings_nim_model(),
        request_id=rid,
    )

    # best-effort telemetry
    repo.insert_run(
        {
            "request_id": rid,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "latency_ms": latency_ms,
            "category": resp.category,
            "priority": resp.priority,
            "tags": resp.tags,
            "model": resp.model,
        }
    )
    return resp


def settings_nim_model() -> str:
    # Avoid importing settings at module import time in some interview scenarios
    from app.core.config import settings
    return settings.nim_model
