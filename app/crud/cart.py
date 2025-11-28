from sqlalchemy.orm import Session
from app.models.cart import Cart

def add_to_cart(db: Session, user_id: int, product_id: int, quantity: int = 1):
    cart_item = Cart(user_id=user_id, product_id=product_id, quantity=quantity)
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return cart_item

def get_cart_items(db: Session, user_id: int):
    return db.query(Cart).filter(Cart.user_id == user_id, Cart.status=="active").all()

def delete_cart_item(db: Session, cart_item_id: int):
    item = db.query(Cart).filter(Cart.id == cart_item_id).first()
    if item:
        db.delete(item)
        db.commit()
    return item

def clear_cart(db: Session, user_id: int):
    db.query(Cart).filter(Cart.user_id == user_id).delete()
    db.commit()
