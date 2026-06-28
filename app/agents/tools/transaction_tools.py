from sqlalchemy.orm import Session

from app.schemas.transaction import TransactionCreate
from app.services.transaction_service import create_transaction, list_transactions


def record_transaction(db: Session, payload: TransactionCreate):
    return create_transaction(db, payload)


def fetch_transactions(db: Session, month: str | None = None):
    return list_transactions(db, month)
