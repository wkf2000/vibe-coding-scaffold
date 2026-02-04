import logging
import sys
import time
from pythonjsonlogger import jsonlogger

from app.core.config import settings


class RedactingJsonFormatter(jsonlogger.JsonFormatter):
    REDACT_KEYS = {"authorization", "api_key", "nim_api_key", "supabase_service_key"}

    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        for k in list(log_record.keys()):
            if k.lower() in self.REDACT_KEYS:
                log_record[k] = "[REDACTED]"


def configure_logging() -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(RedactingJsonFormatter("%(asctime)s %(levelname)s %(name)s %(message)s"))

    root = logging.getLogger()
    root.setLevel(settings.log_level)
    root.handlers = [handler]


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


class Timer:
    def __init__(self) -> None:
        self._start = time.perf_counter()

    def ms(self) -> int:
        return int((time.perf_counter() - self._start) * 1000)
