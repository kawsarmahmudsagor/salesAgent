from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud
from schemas.category import CategoryRead, CategoryUpdate, CategoryCreate
from config.database import get_db
from models.admin import Admin
from services.auth_admin_service import get_current_admin

router = APIRouter(tags=["Categories"])

# Get all categories
@router.get("/", response_model=List[CategoryRead])
def view_categories(db: Session = Depends(get_db)):
    return crud.get_categories(db)

# Get single category
@router.get("/{category_id}", response_model=CategoryRead)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = crud.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

# Create category
@router.post("/", response_model=CategoryRead)
def add_category(category: CategoryCreate, db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_admin)):
    return crud.create_category(db, category)

# Update category
@router.put("/{category_id}", response_model=CategoryRead)
def update_category(category_id: int, category: CategoryUpdate, db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_admin)):
    updated_category = crud.update_category(db, category_id, category)
    if not updated_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated_category

# Delete category
@router.delete("/{category_id}", response_model=CategoryRead)
def remove_category(category_id: int, db: Session = Depends(get_db), current_user: Admin = Depends(get_current_admin)):
    deleted_category = crud.delete_category(db, category_id)
    if not deleted_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return deleted_category
