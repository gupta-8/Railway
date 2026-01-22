import logging
import time
import uuid

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router as api_router
from app.core.logging import configure_logging, set_request_id

configure_logging()
logger = logging.getLogger("railway")

app = FastAPI(
    title="Railway Quest 🚆",
    version="0.2.0",
    description="Mini railway routing + trips + bookings API.",
)

# Request ID + access logging middleware
@app.middleware("http")
async def request_id_and_logging_middleware(request: Request, call_next):
    # Use incoming header if present, otherwise generate one
    request_id = request.headers.get("X-Request-ID") or uuid.uuid4().hex
    set_request_id(request_id)

    start = time.perf_counter()
    try:
        response = await call_next(request)
    finally:
        duration_ms = (time.perf_counter() - start) * 1000.0

    response.headers["X-Request-ID"] = request_id

    logger.info(
        "request completed method=%s path=%s status=%s duration_ms=%.2f",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
