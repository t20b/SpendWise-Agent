import csv
import io
import re
from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate
from app.services.categorization_service import categorize_text, normalize_category

AMOUNT_PATTERN = re.compile(r"([0-9][0-9,]*)\s*(원|krw)?", re.IGNORECASE)


def get_or_create_category(db: Session, category_name: str) -> Category:
    category = db.query(Category).filter(Category.name == category_name).first()
    if category:
        return category
    category = Category(name=category_name, is_default=False)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def create_transaction(db: Session, payload: TransactionCreate) -> Transaction:
    category_name = normalize_category(payload.category) if payload.category else categorize_text(f"{payload.merchant} {payload.description or ''}")
    category = get_or_create_category(db, category_name)
    transaction = Transaction(
        amount=payload.amount,
        merchant=payload.merchant,
        description=payload.description,
        transaction_date=payload.transaction_date,
        payment_method=payload.payment_method,
        source=payload.source,
        category_id=category.id,
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


def list_transactions(db: Session, month: str | None = None) -> list[Transaction]:
    query = db.query(Transaction).join(Category).order_by(Transaction.transaction_date.desc(), Transaction.id.desc())
    if month:
        query = query.filter(Transaction.transaction_date >= date.fromisoformat(f"{month}-01"))
        year, month_num = map(int, month.split("-"))
        next_month = date(year + (month_num == 12), 1 if month_num == 12 else month_num + 1, 1)
        query = query.filter(Transaction.transaction_date < next_month)
    return query.all()


def parse_natural_language_transaction(text: str, today: date | None = None) -> TransactionCreate:
    today = today or date.today()
    match = AMOUNT_PATTERN.search(text)
    if not match:
        raise ValueError("금액을 찾을 수 없습니다. 예: '오늘 스타벅스에서 6500원 썼어'")
    amount = int(match.group(1).replace(",", ""))
    tx_date = today
    if "어제" in text:
        tx_date = today - timedelta(days=1)
    merchant_text = text[: match.start()].strip() or text[match.end() :].strip() or "알 수 없음"
    merchant_text = re.sub(r"^(오늘|어제|내가|나는)\s*", "", merchant_text)
    merchant_text = re.sub(r"에서$", "", merchant_text).strip()
    merchant = merchant_text or "알 수 없음"
    return TransactionCreate(
        amount=amount,
        merchant=merchant,
        transaction_date=tx_date,
        category=categorize_text(text),
        description=text,
        source="natural_language",
    )


def import_transactions_csv(db: Session, content: bytes) -> tuple[int, int, list[Transaction]]:
    decoded = content.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(decoded))
    imported: list[Transaction] = []
    skipped = 0
    for row in reader:
        try:
            payload = TransactionCreate(
                amount=int(str(row.get("amount", "")).replace(",", "")),
                merchant=row.get("merchant") or row.get("description") or "알 수 없음",
                transaction_date=date.fromisoformat(row.get("transaction_date") or row.get("date") or ""),
                category=row.get("category") or None,
                description=row.get("description") or None,
                payment_method=row.get("payment_method") or None,
                source="csv",
            )
        except (TypeError, ValueError):
            skipped += 1
            continue
        imported.append(create_transaction(db, payload))
    return len(imported), skipped, imported
