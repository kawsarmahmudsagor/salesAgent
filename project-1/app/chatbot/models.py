from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.database import Base  # exact import from your project

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    role = Column(String(16))  # user / bot
    message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class Feedback(Base):
    __tablename__ = "feedbacks"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    product_id = Column(Integer, index=True)
    rating = Column(Integer)  # 1-5
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class PolicyDocument(Base):
    __tablename__ = "policy_documents"
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    body = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    embedding_vector = Column(Text, nullable=True)  # optional JSON-encoded embedding
