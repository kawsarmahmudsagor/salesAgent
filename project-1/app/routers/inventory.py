# app/routers/inventory.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud, models
from app.schemas import InventoryDeleteRead
from ..database import get_db
from ..auth import get_current_user

router = APIRouter(tags=["inventory"])

@router.post("/", response_model=schemas.InventoryRead)
def create_inventory(inv_in: schemas.InventoryCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # Optionally validate product exists
    p = crud.get_product(db, inv_in.product_id)
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    return crud.create_inventory(db, inv_in)

@router.get("/product/{product_id}", response_model=List[schemas.InventoryRead])
def list_inventory(product_id: int, db: Session = Depends(get_db)):
    return crud.list_inventory_for_product(db, product_id)

@router.delete("/{inventory_id}", response_model=InventoryDeleteRead)
def remove_inventory(inventory_id: int, db: Session = Depends(get_db)):
    inventory = crud.delete_inventory(db, inventory_id)
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return inventory

