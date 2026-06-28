from sqlalchemy.orm import Session

from app.services.analysis_service import get_monthly_spending_summary
from app.services.budget_service import get_budget_status


def fetch_monthly_summary(db: Session, month: str) -> dict:
    return get_monthly_spending_summary(db, month)


def fetch_budget_status(db: Session, month: str) -> dict:
    return get_budget_status(db, month)
