# app/routers/inventory.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.crud.inventory import create_inventory, list_inventory_for_product, delete_inventory
from app.crud.product import get_product
from app.models.inventory import Inventory
from app.models.admin import Admin
from app.schemas.inventory import InventoryRead, InventoryDeleteRead, InventoryCreate
from app.config.database import get_db
from app.services.auth_admin_service import get_current_admin


router = APIRouter(tags=["inventory"])

@router.post("/", response_model=InventoryRead)
def create_inventory(inv_in: InventoryCreate, db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_admin)):
    # Optionally validate product exists
    p = get_product(db, inv_in.product_id)
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    return create_inventory(db, inv_in)

@router.get("/product/{product_id}", response_model=List[InventoryRead])
def list_inventory(product_id: int, db: Session = Depends(get_db)):
    return list_inventory_for_product(db, product_id)

@router.delete("/{inventory_id}", response_model=InventoryDeleteRead)
def remove_inventory(inventory_id: int, db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_admin)):
    inventory = delete_inventory(db, inventory_id)
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return inventory

