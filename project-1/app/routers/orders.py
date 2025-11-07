# app/routers/orders.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud, models
from ..database import get_db
from ..auth import get_current_user
from typing import List

router = APIRouter()

@router.get("/", response_model=List[schemas.OrderRead])
def list_my_orders(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    orders = crud.get_orders_for_user(db, current_user.id)
    return orders

@router.get("/{order_id}", response_model=schemas.OrderRead)
def get_order(order_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    order = crud.get_order(db, order_id)
    if not order or order.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
