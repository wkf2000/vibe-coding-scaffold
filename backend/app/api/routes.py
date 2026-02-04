from fastapi import APIRouter, Header

from app.schemas.enrich import EnrichRequest, EnrichResponse
from app.services.enrich_service import enrich_text

router = APIRouter()


@router.post("/enrich", response_model=EnrichResponse)
async def enrich(req: EnrichRequest, x_request_id: str | None = Header(default=None)) -> EnrichResponse:
    return await enrich_text(req, request_id=x_request_id)


@router.get("/whoami")
async def whoami() -> dict:
    return {"service": "genai-service", "version": "0.1.0"}
