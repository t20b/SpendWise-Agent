from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class TransactionCreate(BaseModel):
    amount: int = Field(gt=0)
    merchant: str = Field(min_length=1, max_length=120)
    transaction_date: date
    category: str | None = None
    description: str | None = None
    payment_method: str | None = None
    source: str = "manual"


class NaturalLanguageTransactionCreate(BaseModel):
    text: str = Field(min_length=1)


class TransactionRead(BaseModel):
    id: int
    amount: int
    merchant: str
    transaction_date: date
    category: str
    description: str | None
    payment_method: str | None
    source: str

    model_config = ConfigDict(from_attributes=True)


class CsvImportResult(BaseModel):
    imported: int
    skipped: int
    transactions: list[TransactionRead]
