from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.insight import CoachingResponse, MonthlySummaryRead
from app.services.analysis_service import get_monthly_spending_summary
from app.services.report_service import generate_coaching_message

router = APIRouter(prefix="/insights", tags=["insights"])


@router.get("/{month}/summary", response_model=MonthlySummaryRead)
def monthly_summary(month: str, db: Session = Depends(get_db)):
    return get_monthly_spending_summary(db, month)


@router.get("/{month}/coaching", response_model=CoachingResponse)
def monthly_coaching(month: str, db: Session = Depends(get_db)):
    return CoachingResponse(message=generate_coaching_message(db, month), summary=get_monthly_spending_summary(db, month))
