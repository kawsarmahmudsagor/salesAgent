# app/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

# ----------------- ENUMS -----------------
class TrnTypeEnum(str, Enum):
    payment = "payment"
    refund = "refund"
    adjustment = "adjustment"

# ----------------- COMPANY -----------------
class CompanyBase(BaseModel):
    name: str
    description: Optional[str]

class CompanyCreate(CompanyBase):
    pass

class CompanyRead(CompanyBase):
    id: int
    class Config:
        orm_mode = True

# ----------------- PRODUCT TYPE -----------------
class ProductTypeBase(BaseModel):
    name: str

class ProductTypeCreate(ProductTypeBase):
    pass

class ProductTypeRead(ProductTypeBase):
    id: int
    class Config:
        orm_mode = True

# ----------------- CATEGORY -----------------
class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    id: int
    class Config:
        orm_mode = True

# ----------------- PRODUCT -----------------
class ProductBase(BaseModel):
    name: str
    details: Optional[str]
    company_id: Optional[int]        
    product_type_id: Optional[int]
    category_id: Optional[int]
    price: float
    picture: Optional[str]             

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: int
    class Config:
        orm_mode = True

# ----------------- INVENTORY -----------------
class InventoryBase(BaseModel):
    product_id: int
    color: Optional[str]
    size: Optional[str]
    quantity: int

class InventoryCreate(InventoryBase):
    pass

class InventoryRead(InventoryBase):
    id: int
    class Config:
        orm_mode = True

# ----------------- USER -----------------
class UserBase(BaseModel):
    email: EmailStr
    first_name: str           # required
    last_name: Optional[str]
    address: str              # required
    contact_no: str           # required
    picture: Optional[str]

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    class Config:
        orm_mode = True

# ----------------- CART -----------------
class CartItemBase(BaseModel):
    product_id: int
    quantity: int
    status: Optional[str] = "active"

class CartItemCreate(CartItemBase):
    pass

class CartItemRead(CartItemBase):
    id: int
    class Config:
        orm_mode = True

class CartRead(BaseModel):
    id: int
    user_id: int
    items: List[CartItemRead] = []
    class Config:
        orm_mode = True

# ----------------- ORDER -----------------
class OrderCreate(BaseModel):
    user_id: int
    total_amount: float
    user_address: str         # required

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemRead(OrderItemBase):
    id: int
    class Config:
        orm_mode = True

class OrderRead(OrderCreate):
    id: int
    created_at: datetime
    items: List[OrderItemRead] = []
    class Config:
        orm_mode = True

# ----------------- TRANSACTION -----------------
class ProductTransactionBase(BaseModel):
    order_id: Optional[int]
    user_id: int
    trn_type: TrnTypeEnum = TrnTypeEnum.payment
    trn_amount: float
    credit_amount: Optional[float] = 0.0
    debit_amount: Optional[float] = 0.0
    payment_gateway_trn_id: Optional[str]
    payment_method: Optional[str]

class ProductTransactionCreate(ProductTransactionBase):
    pass

class ProductTransactionRead(ProductTransactionBase):
    id: int
    created_at: datetime
    created_by: str
    class Config:
        orm_mode = True
