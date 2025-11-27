from pydantic import BaseModel
from typing import Optional
from product import ProductRead

class CartBase(BaseModel):
    user_id: int
    product_id: int
    quantity: int = 1
    status: Optional[str] = "active"

class CartRead(CartBase):
    id: int
    product: ProductRead
    class Config:
        orm_mode = True