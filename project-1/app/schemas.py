from pydantic import BaseModel, EmailStr
from typing import Optional, List
from enum import Enum
from datetime import datetime

# ---------- ENUMS ----------
class TrnTypeEnum(str, Enum):
    payment = "payment"
    refund = "refund"
    adjustment = "adjustment"

# ---------- USER ----------
class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: Optional[str]
    address: str
    contact_no: str

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    class Config:
        orm_mode = True

# ---------- PRODUCT ----------
class ProductBase(BaseModel):
    name: str
    details: Optional[str]
    price: float
    discount: Optional[float]
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

# ---------- INVENTORY ----------
class InventoryCreate(BaseModel):
    product_id: int
    color: Optional[str] = None
    size: Optional[str] = None
    quantity: int = 0

class InventoryRead(InventoryCreate):
    id: int
    class Config:
        orm_mode = True


# ---------- CART ----------
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

# ---------- ORDER ----------
class OrderBase(BaseModel):
    user_id: int
    total_amount: float
    user_address: str

class OrderRead(OrderBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True

# ---------- ORDER ITEM ----------
class OrderItemBase(BaseModel):
    order_id: int
    product_id: int
    quantity: int = 1

class OrderItemRead(OrderItemBase):
    id: int
    class Config:
        orm_mode = True

# ---------- TRANSACTION ----------
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
