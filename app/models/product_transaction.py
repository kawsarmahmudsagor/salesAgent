from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.config.database import Base
from transaction import TrnTypeEnum

class ProductTransaction(Base):
    __tablename__ = "product_transactions"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    trn_type = Column(Enum(TrnTypeEnum), default=TrnTypeEnum.payment)
    trn_amount = Column(Float, default=0.0)
    credit_amount = Column(Float, default=0.0)
    debit_amount = Column(Float, default=0.0)
    payment_gateway_trn_id = Column(String, nullable=True)
    payment_method = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, nullable=False)

    order = relationship("Order", back_populates="transactions")
    user = relationship("User", back_populates="transactions")