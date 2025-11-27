from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import get_db
from services.auth_admin_service import get_current_admin
from services.auth_user_service import get_current_user
from services.chatbot_service import handle_conversation
from models.user import User
from models.admin import Admin
from models.conversation_history import ConversationHistory
from services import auth_admin_service, auth_user_service
from schemas.chatmodel import ChatRequest


router = APIRouter(tags=["Chatbot"])

@router.post("/")
def chatbot_interaction_user(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_user_service.get_current_user)
):
    # Load last conversation for this user, or create new
    conversation = (
        db.query(ConversationHistory)
        .filter(ConversationHistory.user_id == current_user.id)
        .order_by(ConversationHistory.id.desc())
        .first()
    )

    if not conversation:
        conversation = ConversationHistory(user_id=current_user.id, history="")
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    # Use the conversation history
    history = conversation.history

    # Generate AI reply and updated history
    ai_reply, updated_history = handle_conversation(history, request.message)

    # Save updated conversation
    conversation.history = updated_history
    db.commit()

    return {
        "response": ai_reply,
        "conversation_id": conversation.id
    }


@router.post("/admin")
def chatbot_interaction_admin(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(auth_admin_service.get_current_admin)
):
    # Load last conversation for this user, or create new
    conversation = (
        db.query(ConversationHistory)
        .filter(ConversationHistory.admin_id == current_admin.id)
        .order_by(ConversationHistory.id.desc())
        .first()
    )

    if not conversation:
        conversation = ConversationHistory(admin_id=current_admin.id, history="")
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    # Use the conversation history
    history = conversation.history

    # Generate AI reply and updated history
    ai_reply, updated_history = handle_conversation(history, request.message)

    # Save updated conversation
    conversation.history = updated_history
    db.commit()

    return {
        "response": ai_reply,
        "conversation_id": conversation.id
    }

