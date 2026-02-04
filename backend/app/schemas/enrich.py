from pydantic import BaseModel, Field


class EnrichRequest(BaseModel):
    text: str = Field(min_length=1, max_length=8000)
    locale: str = Field(default="en-US")


class EnrichResponse(BaseModel):
    summary: str
    category: str
    priority: str
    tags: list[str]
    action_items: list[str]
    model: str
    request_id: str | None = None
