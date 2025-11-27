from pydantic import BaseModel
from typing import Optional

class ProductTypeBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProductTypeCreate(ProductTypeBase):
    pass

class ProductTypeUpdate(ProductTypeBase):
    pass

class ProductTypeRead(ProductTypeBase):
    id: int
    class Config:
        orm_mode = True