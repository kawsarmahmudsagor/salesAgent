from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, models, schemas
from ..database import get_db
from ..auth import get_current_user

router = APIRouter(tags=["Product-Types"])

# Get all product types
@router.get("/", response_model=List[schemas.ProductTypeRead])
def view_product_types(db: Session = Depends(get_db)):
    return crud.get_product_types(db)

# Get single product type
@router.get("/{product_type_id}", response_model=schemas.ProductTypeRead)
def get_product_type(product_type_id: int, db: Session = Depends(get_db)):
    product_type = crud.get_product_type(db, product_type_id)
    if not product_type:
        raise HTTPException(status_code=404, detail="Product type not found")
    return product_type

# Create product type
@router.post("/", response_model=schemas.ProductTypeRead)
def add_product_type(product_type: schemas.ProductTypeCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_product_type(db, product_type)

# Update product type
@router.put("/{product_type_id}", response_model=schemas.ProductTypeRead)
def update_product_type(product_type_id: int, product_type: schemas.ProductTypeUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    updated_ptype = crud.update_product_type(db, product_type_id, product_type)
    if not updated_ptype:
        raise HTTPException(status_code=404, detail="Product type not found")
    return updated_ptype

# Delete product type
@router.delete("/{product_type_id}", response_model=schemas.ProductTypeRead)
def remove_product_type(product_type_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    deleted_ptype = crud.delete_product_type(db, product_type_id)
    if not deleted_ptype:
        raise HTTPException(status_code=404, detail="Product type not found")
    return deleted_ptype

