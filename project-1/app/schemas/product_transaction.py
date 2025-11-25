from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from transaction_type import TrnTypeEnum

class ProductTransactionBase(BaseModel):
    order_id: Optional[int]
    user_id: int
    trn_type: TrnTypeEnum = TrnTypeEnum.payment
    trn_amount: float
    credit_amount: Optional[float] = 0.0
    debit_amount: Optional[float] = 0.0
    payment_gateway_trn_id: Optional[str]
    payment_method: Optional[str]
    created_by: str

class ProductTransactionRead(ProductTransactionBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True
