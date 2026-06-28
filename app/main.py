from fastapi import FastAPI

from app.api.routes import budgets, categories, chat, insights, transactions
from app.core.config import get_settings
from app.db.init_db import create_db_and_tables, seed_default_categories
from app.db.session import SessionLocal

settings = get_settings()
app = FastAPI(title=settings.app_name)


@app.on_event("startup")
def on_startup() -> None:
    create_db_and_tables()
    db = SessionLocal()
    try:
        seed_default_categories(db)
    finally:
        db.close()


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(categories.router)
app.include_router(transactions.router)
app.include_router(budgets.router)
app.include_router(insights.router)
app.include_router(chat.router)
