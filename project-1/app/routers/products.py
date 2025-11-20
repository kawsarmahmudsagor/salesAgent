from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import crud, models, schemas
from ..database import get_db
from ..auth import get_current_user
import os
import shutil


router = APIRouter(tags=["Products"])

# Get all products with optional filters
@router.get("/", response_model=List[schemas.ProductRead])
def view_products(
    size: Optional[str] = None,
    color: Optional[str] = None,
    min_price: float = 0,
    max_price: float = 1e10,
    company_id: Optional[int] = None,  
    db: Session = Depends(get_db)
):
    return crud.get_products(
        db, 
        size=size, 
        color=color, 
        min_price=min_price, 
        max_price=max_price, 
        company_id=company_id
    )


# Get single product by ID
@router.get("/{product_id}", response_model=schemas.ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Add a new product
@router.post("/", response_model=schemas.ProductRead)
def add_product(
    name: str,
    price: float,
    size: int,
    details: Optional[str] = None,
    discount: Optional[float] = 0.0,
    company_id: Optional[int] = None,
    product_type_id: Optional[int] = None,
    category_id: Optional[int] = None,
    picture: Optional[UploadFile] = File(None),

    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Handle picture upload
    picture_path = None
    if picture:
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)

        picture_path = os.path.join(upload_dir, picture.filename)
        with open(picture_path, "wb") as buffer:
            shutil.copyfileobj(picture.file, buffer)

    product_data = schemas.ProductCreate(
        name=name,
        size=size,
        price=price,
        details=details,
        discount=discount,
        picture=picture_path,
        company_id=company_id,
        product_type_id=product_type_id,
        category_id=category_id
    )

    return crud.create_product(db, product_data)


# Delete a product
@router.delete("/{product_id}", response_model=schemas.ProductRead)
def remove_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    product = crud.delete_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
