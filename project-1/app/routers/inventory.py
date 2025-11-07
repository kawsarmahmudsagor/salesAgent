# app/routers/inventory.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud, models
from ..database import get_db
from ..auth import get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.InventoryRead)
def create_inventory(inventory_in: schemas.InventoryCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # Optionally validate product exists
    product = crud.get_product(db, inventory_in.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return crud.create_inventory(db, inventory_in)

@router.get("/product/{product_id}", response_model=List[schemas.InventoryRead])
def list_of_inventory(product_id: int, db: Session = Depends(get_db)):
    return crud.list_of_inventory_for_product(db, product_id)
