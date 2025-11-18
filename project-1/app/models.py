# app/models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
import enum

class TrnTypeEnum(str, enum.Enum):
    payment = "payment"
    refund = "refund"
    adjustment = "adjustment"

#Company Table
class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    
    products = relationship("Product", back_populates="company")

# PRODUCT-TYPE Table
class ProductType(Base):
    __tablename__ = "product_types"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    products = relationship("Product", back_populates="product_type")

# PRODUCT-CATEGORY Table
class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    products = relationship("Product", back_populates="category")

#PRODUCT Table
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index = True)
    name = Column(String, nullable=False)
    details = Column(Text)
    price = Column(Float, nullable=False, default=0.0)
    discount = Column(Float, nullable=True, default=0.0)
    picture = Column(String, nullable=True) #picture optional field, can be adjusted later
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
    product_type_id = Column(Integer, ForeignKey("product_types.id"), nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
     
    company = relationship("Company", back_populates="products")
    product_type = relationship("ProductType", back_populates="products")
    category = relationship("Category", back_populates="products")

    inventory_items = relationship("Inventory", back_populates="product")
    cart_items = relationship("Cart", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")

    @property
    def final_price(self):
        return self.price * (1 - self.discount / 100)



#INVENTORY Table
class Inventory(Base):
    __tablename__ = "inventories"
    id = Column(Integer, primary_key=True, index=True)
    color = Column(String, nullable=True)
    size = Column(String, nullable=True)
    quantity = Column(Integer, default=0)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False) 

    product = relationship("Product", back_populates="inventory_items")

#USER Table
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index = True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False) 
    last_name = Column(String, nullable=True)
    address = Column(Text, nullable=False)       
    contact_no = Column(String, nullable=False)  
    picture = Column(String, nullable=True)

    cart = relationship("Cart", back_populates="user")
    orders = relationship("Order", back_populates="user")
    transactions = relationship("ProductTransaction", back_populates="user")


class Cart(Base):
    __tablename__ = "cart_items"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, default=1)
    status = Column(String, default="active")  # active/removed/saved

    user = relationship("User", back_populates="cart")
    product = relationship("Product", back_populates="cart_items")

# ORDER Table
class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_amount = Column(Float, nullable=False)
    user_address = Column(Text, nullable=False)  
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    transactions = relationship("ProductTransaction", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, default=1)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")

# TRANSACTION
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



