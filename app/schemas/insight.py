from pydantic import BaseModel


class MonthlySummaryRead(BaseModel):
    month: str
    total_spent: int
    by_category: dict[str, int]
    top_categories: list[tuple[str, int]]


class CoachingResponse(BaseModel):
    message: str
    summary: MonthlySummaryRead | None = None
