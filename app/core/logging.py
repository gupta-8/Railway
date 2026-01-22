from __future__ import annotations

import logging
import os
from contextvars import ContextVar

# Context variable to carry request id across async calls
_request_id_ctx: ContextVar[str] = ContextVar("request_id", default="-")


def get_request_id() -> str:
    return _request_id_ctx.get()


def set_request_id(request_id: str) -> None:
    _request_id_ctx.set(request_id)


class RequestIdFilter(logging.Filter):
    """Injects request_id into every log record."""
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = get_request_id()
        return True


def configure_logging() -> None:
    """
    Simple structured-ish logging using standard logging.
    Adds request_id to every log line via a logging Filter.

    Env vars:
      - LOG_LEVEL (default: INFO)
    """
    level_str = os.getenv("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_str, logging.INFO)

    # NOTE: keep it plain and reliable; works locally + in containers
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s [%(request_id)s] %(name)s: %(message)s",
    )

    # Attach filter to root logger so all loggers inherit it
    root = logging.getLogger()
    root.addFilter(RequestIdFilter())
