from pydantic import BaseModel
from typing import Optional
from app.schemas.product import ProductRead


class InventoryBase(BaseModel):
    product_id: int
    color: Optional[str] = None
    quantity: int = 0

class InventoryCreate(InventoryBase):
    pass

class InventoryRead(InventoryBase):
    id: int
    product: ProductRead
    class Config:
        orm_mode = True

class InventoryDeleteRead(BaseModel):
    id: int
    product_id: int
    color: Optional[str] = None
    quantity: int = 0

    class Config:
        orm_mode = True