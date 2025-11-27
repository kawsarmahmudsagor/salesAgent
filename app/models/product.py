from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, DateTime, Enum
from sqlalchemy.orm import relationship
from app.config.database import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    details = Column(Text, nullable=True)
    price = Column(Float, nullable=False, default=0.0)
    discount = Column(Float, nullable=True, default=0.0)
    picture = Column(String, nullable=True)
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
        return self.price * (1 - (self.discount or 0) / 100)