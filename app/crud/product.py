from sqlalchemy.orm import Session
from models.product import Product
from models.inventory import Inventory
from schemas.product import ProductCreate
from typing import List, Optional

def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def get_products(
    db: Session, 
    size: Optional[str] = None, 
    color: Optional[str] = None, 
    min_price: float = 0, 
    max_price: float = 1e10, 
    company_id: Optional[int] = None
):
    query = db.query(Product)

    # Join inventory only if filtering by size or color
    if size or color:
        query = query.join(Inventory)
        if size:
            query = query.filter(Inventory.size == size)
        if color:
            query = query.filter(Inventory.color == color)

    # Filter by price
    query = query.filter(Product.price >= min_price, Product.price <= max_price)

    # Filter by company if specified
    if company_id:
        query = query.filter(Product.company_id == company_id)

    # Return all products if no filters specified
    return query.all()


def create_product(db: Session, product: ProductCreate):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
    return product