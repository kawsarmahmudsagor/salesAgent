from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, models, schemas
from ..database import get_db
from ..auth import get_current_user

router = APIRouter(tags=["Categories"])

# Get all categories
@router.get("/", response_model=List[schemas.CategoryRead])
def view_categories(db: Session = Depends(get_db)):
    return crud.get_categories(db)

# Get single category
@router.get("/{category_id}", response_model=schemas.CategoryRead)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = crud.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

# Create category
@router.post("/", response_model=schemas.CategoryRead)
def add_category(category: schemas.CategoryCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_category(db, category)

# Update category
@router.put("/{category_id}", response_model=schemas.CategoryRead)
def update_category(category_id: int, category: schemas.CategoryUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    updated_category = crud.update_category(db, category_id, category)
    if not updated_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated_category

# Delete category
@router.delete("/{category_id}", response_model=schemas.CategoryRead)
def remove_category(category_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    deleted_category = crud.delete_category(db, category_id)
    if not deleted_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return deleted_category
