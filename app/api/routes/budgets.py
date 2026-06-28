from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.budget import BudgetProfileUpsert, BudgetStatusRead
from app.services.budget_service import get_budget_status, upsert_budget_profile

router = APIRouter(prefix="/budgets", tags=["budgets"])


@router.put("/{month}", response_model=BudgetStatusRead)
def upsert_budget(month: str, payload: BudgetProfileUpsert, db: Session = Depends(get_db)):
    payload.month = month
    upsert_budget_profile(db, payload)
    return get_budget_status(db, month)


@router.get("/{month}", response_model=BudgetStatusRead)
def read_budget_status(month: str, db: Session = Depends(get_db)):
    return get_budget_status(db, month)
