from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.session import engine
from app.models.category import Category

DEFAULT_CATEGORIES = [
    "식비",
    "카페/간식",
    "교통",
    "쇼핑",
    "생활용품",
    "주거",
    "통신",
    "구독",
    "의료",
    "문화/여가",
    "교육",
    "여행",
    "금융/보험",
    "기타",
]


def create_db_and_tables() -> None:
    Base.metadata.create_all(bind=engine)


def seed_default_categories(db: Session) -> None:
    existing = {name for (name,) in db.query(Category.name).all()}
    for name in DEFAULT_CATEGORIES:
        if name not in existing:
            db.add(Category(name=name, is_default=True))
    db.commit()
