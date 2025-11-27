from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name: str
    details: Optional[str]
    size: int
    price: float
    discount: Optional[float] = 0.0
    picture: Optional[str] = None
    company_id: Optional[int]
    product_type_id: Optional[int]
    category_id: Optional[int]

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: int
    class Config:
        orm_mode = True