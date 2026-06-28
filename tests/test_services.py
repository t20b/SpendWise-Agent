from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.init_db import seed_default_categories
from app.schemas.budget import BudgetProfileUpsert
from app.schemas.transaction import TransactionCreate
from app.services.analysis_service import get_monthly_spending_summary
from app.services.budget_service import get_budget_status, upsert_budget_profile
from app.services.transaction_service import create_transaction, parse_natural_language_transaction


def make_db():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    db = Session()
    seed_default_categories(db)
    return db


def test_parse_natural_language_transaction():
    payload = parse_natural_language_transaction("오늘 스타벅스에서 6,500원 썼어", today=date(2026, 6, 28))
    assert payload.amount == 6500
    assert payload.transaction_date == date(2026, 6, 28)
    assert payload.category == "카페/간식"


def test_monthly_summary_and_budget_status():
    db = make_db()
    create_transaction(db, TransactionCreate(amount=6500, merchant="스타벅스", transaction_date=date(2026, 6, 28)))
    create_transaction(db, TransactionCreate(amount=12000, merchant="김밥집", transaction_date=date(2026, 6, 28)))
    upsert_budget_profile(
        db,
        BudgetProfileUpsert(
            month="2026-06",
            monthly_income=3_000_000,
            monthly_savings_goal=500_000,
            monthly_total_budget=1_000_000,
            category_budgets={"카페/간식": 50_000, "식비": 600_000},
        ),
    )

    summary = get_monthly_spending_summary(db, "2026-06")
    assert summary["total_spent"] == 18500
    assert summary["by_category"]["카페/간식"] == 6500

    status = get_budget_status(db, "2026-06")
    assert status["total_remaining"] == 981500
    assert status["total_usage_rate"] == 1.9
