from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..auth import get_current_user
from .. import chatbot, models
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str

router = APIRouter(tags=["Chatbot"])

@router.post("/")
def chatbot_interaction(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Load last conversation for this user, or create new
    conversation = (
        db.query(models.ConversationHistory)
        .filter(models.ConversationHistory.user_id == current_user.id)
        .order_by(models.ConversationHistory.id.desc())
        .first()
    )

    if not conversation:
        conversation = models.ConversationHistory(user_id=current_user.id, history="")
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    # Use the conversation history
    history = conversation.history

    # Generate AI reply and updated history
    ai_reply, updated_history = chatbot.handle_conversation(history, request.message)

    # Save updated conversation
    conversation.history = updated_history
    db.commit()

    return {
        "response": ai_reply,
        "conversation_id": conversation.id
    }

