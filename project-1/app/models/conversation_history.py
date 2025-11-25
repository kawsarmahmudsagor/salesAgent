from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, DateTime, Enum
from sqlalchemy.orm import relationship
from app.config.database import Base

class ConversationHistory(Base):
    __tablename__ = "conversation_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    admin_id = Column(Integer, ForeignKey("admins.id"))
    history = Column(Text, default="")

    # Each conversation belongs to a single user
    user = relationship("User", back_populates="conversations")
    admin = relationship("Admin", back_populates="conversations")