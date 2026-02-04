from __future__ import annotations

from typing import Any

from supabase import Client, create_client

from app.core.config import settings
from app.core.logging import get_logger

log = get_logger(__name__)


class SupabaseRepo:
    def __init__(self) -> None:
        self._enabled = bool(settings.supabase_url and settings.supabase_service_key)
        self._table = settings.supabase_table_runs
        self._client: Client | None = None
        if self._enabled:
            self._client = create_client(settings.supabase_url, settings.supabase_service_key)

    def enabled(self) -> bool:
        return self._enabled and self._client is not None

    def insert_run(self, row: dict[str, Any]) -> None:
        if not self.enabled():
            return
        assert self._client is not None
        try:
            self._client.table(self._table).insert(row).execute()
        except Exception:
            log.exception("supabase_insert_failed", extra={"table": self._table})
