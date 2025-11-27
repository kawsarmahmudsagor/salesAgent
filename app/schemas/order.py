from pydantic import BaseModel
from datetime import datetime

class OrderBase(BaseModel):
    user_id: int
    total_amount: float
    user_address: str

class OrderRead(OrderBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True