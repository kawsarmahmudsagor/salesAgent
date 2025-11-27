from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from config.database import get_db
from models.admin import Admin
from schemas.product_type import ProductTypeRead, ProductTypeUpdate, ProductTypeCreate
from crud.product_type import get_product_type, get_product_types, create_product_type, delete_product_type
from services.auth_admin_service import get_current_admin

router = APIRouter(tags=["Product-Types"])

# Get all product types
@router.get("/", response_model=List[ProductTypeRead])
def view_product_types(db: Session = Depends(get_db)):
    return get_product_types(db)

# Get single product type
@router.get("/{product_type_id}", response_model=ProductTypeRead)
def get_product_type(product_type_id: int, db: Session = Depends(get_db)):
    product_type = get_product_type(db, product_type_id)
    if not product_type:
        raise HTTPException(status_code=404, detail="Product type not found")
    return product_type

# Create product type
@router.post("/", response_model=ProductTypeRead)
def add_product_type(product_type: ProductTypeCreate, db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_admin)):
    return create_product_type(db, product_type)

# Update product type
@router.put("/{product_type_id}", response_model=ProductTypeRead)
def update_product_type(product_type_id: int, product_type: ProductTypeUpdate, db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_admin)):
    updated_ptype = update_product_type(db, product_type_id, product_type)
    if not updated_ptype:
        raise HTTPException(status_code=404, detail="Product type not found")
    return updated_ptype

# Delete product type
@router.delete("/{product_type_id}", response_model= ProductTypeRead)
def remove_product_type(product_type_id: int, db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_admin)):
    deleted_ptype = delete_product_type(db, product_type_id)
    if not deleted_ptype:
        raise HTTPException(status_code=404, detail="Product type not found")
    return deleted_ptype

