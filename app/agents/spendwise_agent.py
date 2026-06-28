from datetime import date

from sqlalchemy.orm import Session

from app.schemas.transaction import TransactionCreate
from app.services.report_service import generate_coaching_message
from app.services.transaction_service import create_transaction, parse_natural_language_transaction


class SpendWiseAgent:
    """Rule-backed MVP agent for parsing spending text and producing coaching."""

    def parse_transaction(self, text: str, today: date | None = None) -> TransactionCreate:
        return parse_natural_language_transaction(text, today=today)

    def record_from_text(self, db: Session, text: str) -> str:
        payload = self.parse_transaction(text)
        transaction = create_transaction(db, payload)
        return f"{transaction.transaction_date.isoformat()} {transaction.merchant} 지출 {transaction.amount:,}원을 {transaction.category.name} 카테고리로 기록했습니다."

    def coach(self, db: Session, month: str | None = None) -> str:
        target_month = month or date.today().strftime("%Y-%m")
        return generate_coaching_message(db, target_month)

    def chat(self, db: Session, message: str, month: str | None = None) -> str:
        if any(keyword in message for keyword in ["썼", "사용", "결제", "소비"]) and any(char.isdigit() for char in message):
            try:
                return self.record_from_text(db, message)
            except ValueError:
                pass
        return self.coach(db, month=month)
