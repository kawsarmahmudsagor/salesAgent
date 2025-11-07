# app/routers/products.py
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from .. import schemas, crud, models
from ..database import get_db
from ..auth import get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.ProductRead)
def create_product(product_in: schemas.ProductCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # For now any authenticated user can create products.
    return crud.create_product(db, product_in)

@router.get("/", response_model=List[schemas.ProductRead])
def list_of_products(
    size: Optional[str] = Query(None),
    color: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    skip: int = 0, limit: int = 50,
    db: Session = Depends(get_db)
):
    products = crud.list_of_products(db, size=size, color=color, min_price=min_price, max_price=max_price, skip=skip, limit=limit)
    return products

@router.get("/{product_id}", response_model=schemas.ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    ok_to_delete = crud.delete_product(db, product_id)
    if not ok_to_delete:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"detail": "Deleted"}
