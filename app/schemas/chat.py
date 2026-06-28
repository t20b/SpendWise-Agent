from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    month: str | None = Field(default=None, pattern=r"^\d{4}-\d{2}$")


class ChatResponse(BaseModel):
    message: str
