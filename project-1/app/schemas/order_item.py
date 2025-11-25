from pydantic import BaseModel

class OrderItemBase(BaseModel):
    order_id: int
    product_id: int
    quantity: int = 1

class OrderItemRead(OrderItemBase):
    id: int
    class Config:
        orm_mode = True