# app/crud.py
from sqlalchemy.orm import Session
from . import models, schemas
from typing import List, Optional

# ----------------- PRODUCTS -----------------
def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_products(db: Session, size: Optional[str] = None, color: Optional[str] = None, min_price: float = 0, max_price: float = 1e10):
    query = db.query(models.Product).join(models.Inventory)
    
    if size:
        query = query.filter(models.Inventory.size == size)
    if color:
        query = query.filter(models.Inventory.color == color)
    query = query.filter(models.Product.price >= min_price, models.Product.price <= max_price)
    
    return query.all()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
    return product

# ----------------- CART -----------------
def add_to_cart(db: Session, user_id: int, product_id: int, quantity: int = 1):
    cart_item = models.Cart(user_id=user_id, product_id=product_id, quantity=quantity)
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return cart_item

def get_cart_items(db: Session, user_id: int):
    return db.query(models.Cart).filter(models.Cart.user_id == user_id, models.Cart.status=="active").all()

def delete_cart_item(db: Session, cart_item_id: int):
    item = db.query(models.Cart).filter(models.Cart.id == cart_item_id).first()
    if item:
        db.delete(item)
        db.commit()
    return item

def clear_cart(db: Session, user_id: int):
    db.query(models.Cart).filter(models.Cart.user_id == user_id).delete()
    db.commit()

# ----------------- ORDERS -----------------
def create_order(db: Session, user_id: int, user_address: str, items: List[models.Cart]):
    # Calculate total using discounted price
    total_amount = sum([item.product.final_price * item.quantity for item in items])

    # Create the order
    order = models.Order(user_id=user_id, total_amount=total_amount, user_address=user_address)
    db.add(order)
    db.commit()
    db.refresh(order)

    # Add order items
    for item in items:
        order_item = models.OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(order_item)
    db.commit()
    return order


# ----------------- TRANSACTIONS -----------------
def create_transaction(db: Session, user_id: int, order_id: int, trn_amount: float, created_by: str):
    transaction = models.ProductTransaction(
        user_id=user_id,
        order_id=order_id,
        trn_type=models.TrnTypeEnum.payment,
        trn_amount=trn_amount,
        credit_amount=trn_amount,
        debit_amount=0,
        created_by=created_by
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction
