from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, DateTime, Enum
from sqlalchemy.orm import relationship
from app.config.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    address = Column(Text, nullable=False)
    contact_no = Column(String, nullable=False)
    picture = Column(String, nullable=True)

    cart = relationship("Cart", back_populates="user")
    orders = relationship("Order", back_populates="user")
    transactions = relationship("ProductTransaction", back_populates="user")
    conversations = relationship("ConversationHistory", back_populates="user")