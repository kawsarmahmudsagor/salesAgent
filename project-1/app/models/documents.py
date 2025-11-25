from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, DateTime, Enum
from sqlalchemy.orm import relationship
from app.config.database import Base

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    summary = Column(Text, nullable=False)
    tags = Column(String, nullable=False)
    uploaded_by_id = Column(Integer, ForeignKey("admins.id"), nullable=False)

    uploaded_by = relationship("Admin", back_populates="documents")