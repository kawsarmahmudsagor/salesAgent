# app/routers/cart.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud, models
from ..database import get_db
from ..auth import get_current_user

router = APIRouter()

@router.post("/add", response_model=schemas.CartItemRead)
def add_item_to_cart(item: schemas.CartItemCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # ensure product exists
    product = crud.get_product(db, item.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return crud.add_to_cart(db, current_user.id, item.product_id, item.quantity)

@router.get("/", response_model=schemas.CartRead)
def view_cart(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    cart = crud.get_cart_by_user(db, current_user.id)
    if not cart:
        # create empty cart
        cart = models.Cart(user_id=current_user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    # eager load items
    items = []
    for item in cart.items:
        items.append(item)
    return cart

@router.delete("/item/{item_id}")
def delete_cart_item(item_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # ensure this item belongs to user's cart
    cart = crud.get_cart_by_user(db, current_user.id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    item = db.query(models.CartItem).filter(models.CartItem.id == item_id, models.CartItem.cart_id == cart.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    crud.remove_cart_item(db, item_id)
    return {"detail": "removed"}

@router.delete("/")
def delete_cart(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    cart = crud.get_cart_by_user(db, current_user.id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    crud.delete_cart(db, cart.id)
    return {"detail": "cart deleted"}

class CheckoutRequest(schemas.OrderCreate):
    pass

@router.post("/checkout")
def checkout(payload: CheckoutRequest, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """
    payload expects: user_id (should match current_user.id), total_amount (ignored; computed), user_address
    We'll compute actual total from cart items and create an order + transaction, then delete cart items.
    """
    if payload.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="user_id mismatch")
    try:
        order, trn = crud.checkout_cart(db, current_user, payload.user_address)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"order_id": order.id, "transaction_id": trn.id, "total_amount": order.total_amount}
