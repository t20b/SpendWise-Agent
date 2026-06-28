from sqlalchemy.orm import Session

from app.models.budget import BudgetProfile, CategoryBudget
from app.models.category import Category
from app.schemas.budget import BudgetProfileUpsert
from app.services.analysis_service import get_monthly_spending_summary
from app.services.transaction_service import get_or_create_category


def upsert_budget_profile(db: Session, payload: BudgetProfileUpsert) -> BudgetProfile:
    profile = db.get(BudgetProfile, payload.month)
    if profile is None:
        profile = BudgetProfile(month=payload.month, monthly_income=payload.monthly_income, monthly_savings_goal=payload.monthly_savings_goal, monthly_total_budget=payload.monthly_total_budget)
        db.add(profile)
    else:
        profile.monthly_income = payload.monthly_income
        profile.monthly_savings_goal = payload.monthly_savings_goal
        profile.monthly_total_budget = payload.monthly_total_budget
    for category_name, limit_amount in payload.category_budgets.items():
        category = get_or_create_category(db, category_name)
        budget = db.query(CategoryBudget).filter(CategoryBudget.month == payload.month, CategoryBudget.category_id == category.id).first()
        if budget is None:
            budget = CategoryBudget(month=payload.month, category_id=category.id, limit_amount=limit_amount)
            db.add(budget)
        else:
            budget.limit_amount = limit_amount
    db.commit()
    db.refresh(profile)
    return profile


def get_budget_status(db: Session, month: str) -> dict:
    profile = db.get(BudgetProfile, month)
    if profile is None:
        return {
            "month": month,
            "monthly_income": 0,
            "monthly_savings_goal": 0,
            "monthly_total_budget": 0,
            "total_spent": 0,
            "total_remaining": 0,
            "total_usage_rate": 0,
            "category_budgets": [],
        }
    summary = get_monthly_spending_summary(db, month)
    category_budgets = []
    budgets = db.query(CategoryBudget).join(Category).filter(CategoryBudget.month == month).all()
    for budget in budgets:
        spent = summary["by_category"].get(budget.category.name, 0)
        remaining = budget.limit_amount - spent
        usage_rate = round(spent / budget.limit_amount * 100, 1) if budget.limit_amount else 0
        category_budgets.append({"category": budget.category.name, "limit_amount": budget.limit_amount, "spent_amount": spent, "remaining_amount": remaining, "usage_rate": usage_rate})
    total_spent = summary["total_spent"]
    total_remaining = profile.monthly_total_budget - total_spent
    total_usage_rate = round(total_spent / profile.monthly_total_budget * 100, 1) if profile.monthly_total_budget else 0
    return {"month": month, "monthly_income": profile.monthly_income, "monthly_savings_goal": profile.monthly_savings_goal, "monthly_total_budget": profile.monthly_total_budget, "total_spent": total_spent, "total_remaining": total_remaining, "total_usage_rate": total_usage_rate, "category_budgets": category_budgets}
