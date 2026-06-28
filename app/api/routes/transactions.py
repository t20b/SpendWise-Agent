from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.transaction import CsvImportResult, NaturalLanguageTransactionCreate, TransactionCreate, TransactionRead
from app.services.transaction_service import create_transaction, import_transactions_csv, list_transactions, parse_natural_language_transaction

router = APIRouter(prefix="/transactions", tags=["transactions"])


def to_read(transaction) -> TransactionRead:
    return TransactionRead(
        id=transaction.id,
        amount=transaction.amount,
        merchant=transaction.merchant,
        transaction_date=transaction.transaction_date,
        category=transaction.category.name,
        description=transaction.description,
        payment_method=transaction.payment_method,
        source=transaction.source,
    )


@router.post("", response_model=TransactionRead)
def create_manual_transaction(payload: TransactionCreate, db: Session = Depends(get_db)):
    return to_read(create_transaction(db, payload))


@router.post("/natural-language", response_model=TransactionRead)
def create_natural_language_transaction(payload: NaturalLanguageTransactionCreate, db: Session = Depends(get_db)):
    try:
        parsed = parse_natural_language_transaction(payload.text)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return to_read(create_transaction(db, parsed))


@router.post("/csv", response_model=CsvImportResult)
def import_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    imported, skipped, transactions = import_transactions_csv(db, file.file.read())
    return CsvImportResult(imported=imported, skipped=skipped, transactions=[to_read(tx) for tx in transactions])


@router.get("", response_model=list[TransactionRead])
def get_transactions(month: str | None = None, db: Session = Depends(get_db)):
    return [to_read(tx) for tx in list_transactions(db, month=month)]
