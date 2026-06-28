from datetime import date

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.transaction import Transaction


def month_bounds(month: str) -> tuple[date, date]:
    year, month_num = map(int, month.split("-"))
    start = date(year, month_num, 1)
    end = date(year + (month_num == 12), 1 if month_num == 12 else month_num + 1, 1)
    return start, end


def get_monthly_spending_summary(db: Session, month: str) -> dict:
    start, end = month_bounds(month)
    rows = (
        db.query(Category.name, func.coalesce(func.sum(Transaction.amount), 0))
        .join(Transaction, Transaction.category_id == Category.id)
        .filter(Transaction.transaction_date >= start, Transaction.transaction_date < end)
        .group_by(Category.name)
        .all()
    )
    by_category = {name: int(total) for name, total in rows}
    total_spent = sum(by_category.values())
    top_categories = sorted(by_category.items(), key=lambda item: item[1], reverse=True)[:5]
    return {"month": month, "total_spent": total_spent, "by_category": by_category, "top_categories": top_categories}
