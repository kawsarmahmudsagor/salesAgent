from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, models, schemas
from ..database import get_db
from ..auth import get_current_user

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.post("/", response_model=schemas.CartRead)
def add_cart_item(product_id: int, quantity: int = 1, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.add_to_cart(db, current_user.id, product_id, quantity)

@router.get("/", response_model=List[schemas.CartRead])
def view_cart(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.get_cart_items(db, current_user.id)

@router.delete("/{cart_item_id}", response_model=schemas.CartRead)
def remove_cart_item(cart_item_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    item = crud.delete_cart_item(db, cart_item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return item

@router.post("/checkout", response_model=schemas.OrderRead)
def checkout_cart(user_address: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    cart_items = crud.get_cart_items(db, current_user.id)
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    order = crud.create_order(db, current_user.id, user_address, cart_items)
    crud.create_transaction(db, current_user.id, order.id, order.total_amount, created_by=current_user.email)
    crud.clear_cart(db, current_user.id)
    return order
