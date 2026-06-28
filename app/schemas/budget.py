from pydantic import BaseModel, Field


class BudgetProfileUpsert(BaseModel):
    month: str = Field(pattern=r"^\d{4}-\d{2}$")
    monthly_income: int = Field(ge=0)
    monthly_savings_goal: int = Field(ge=0)
    monthly_total_budget: int = Field(ge=0)
    category_budgets: dict[str, int] = Field(default_factory=dict)


class CategoryBudgetRead(BaseModel):
    category: str
    limit_amount: int
    spent_amount: int = 0
    remaining_amount: int = 0
    usage_rate: float = 0


class BudgetStatusRead(BaseModel):
    month: str
    monthly_income: int
    monthly_savings_goal: int
    monthly_total_budget: int
    total_spent: int
    total_remaining: int
    total_usage_rate: float
    category_budgets: list[CategoryBudgetRead]
