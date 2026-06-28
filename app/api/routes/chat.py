from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.agents.spendwise_agent import SpendWiseAgent
from app.api.deps import get_db
from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter(prefix="/chat", tags=["chat"])
agent = SpendWiseAgent()


@router.post("", response_model=ChatResponse)
def chat(payload: ChatRequest, db: Session = Depends(get_db)):
    return ChatResponse(message=agent.chat(db, payload.message, month=payload.month))
