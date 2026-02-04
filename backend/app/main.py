from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.routes import router as v1_router
from app.core.config import settings
from app.core.errors import AppError
from app.core.logging import configure_logging, get_logger

configure_logging()
log = get_logger(__name__)

app = FastAPI(title="GenAI Service", version="0.1.0")
app.include_router(v1_router, prefix=settings.api_prefix)


@app.get("/healthz")
def healthz() -> dict:
    return {"status": "ok"}


@app.exception_handler(AppError)
async def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"error": exc.code, "message": exc.message})


@app.exception_handler(Exception)
async def unhandled_error_handler(request: Request, exc: Exception) -> JSONResponse:
    log.exception("unhandled_error", extra={"request_id": request.headers.get("x-request-id")})
    return JSONResponse(status_code=500, content={"error": "internal_error", "message": "Internal server error"})
