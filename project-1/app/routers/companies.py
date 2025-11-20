from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, models, schemas
from ..database import get_db
from ..auth import get_current_user

router = APIRouter(tags=["Companies"])

# Get all companies
@router.get("/", response_model=List[schemas.CompanyRead])
def view_companies(db: Session = Depends(get_db)):
    return crud.get_companies(db)

# Get single company
@router.get("/{company_id}", response_model=schemas.CompanyRead)
def get_company(company_id: int, db: Session = Depends(get_db)):
    company = crud.get_company(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

# Create company
@router.post("/", response_model=schemas.CompanyRead)
def add_company(company: schemas.CompanyCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_company(db, company)

# Update company
@router.put("/{company_id}", response_model=schemas.CompanyRead)
def update_company(company_id: int, company: schemas.CompanyUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    updated_company = crud.update_company(db, company_id, company)
    if not updated_company:
        raise HTTPException(status_code=404, detail="Company not found")
    return updated_company

# Delete company
@router.delete("/{company_id}", response_model=schemas.CompanyRead)
def remove_company(company_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    deleted_company = crud.delete_company(db, company_id)
    if not deleted_company:
        raise HTTPException(status_code=404, detail="Company not found")
    return deleted_company
