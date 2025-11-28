from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.crud.company import get_company, get_companies, create_company, update_company, delete_company
from app.schemas.company import CompanyRead, CompanyCreate, CompanyUpdate
from app.models.admin import Admin
from app.config.database import get_db
from app.services import auth_admin_service

router = APIRouter(tags=["Companies"])

# Get all companies
@router.get("/", response_model=List[CompanyRead])
def view_companies(db: Session = Depends(get_db)):
    return get_companies(db)

# Get single company
@router.get("/{company_id}", response_model=CompanyRead)
def get_company(company_id: int, db: Session = Depends(get_db)):
    company = get_company(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

# Create company
@router.post("/", response_model=CompanyRead)
def add_company(company: CompanyCreate, db: Session = Depends(get_db), current_admin: Admin = Depends(auth_admin_service.get_current_admin)):
    return create_company(db, company)

# Update company
@router.put("/{company_id}", response_model=CompanyRead)
def update_company(company_id: int, company: CompanyUpdate, db: Session = Depends(get_db), current_admin: Admin = Depends(auth_admin_service.get_current_admin)):
    updated_company = update_company(db, company_id, company)
    if not updated_company:
        raise HTTPException(status_code=404, detail="Company not found")
    return updated_company

# Delete company
@router.delete("/{company_id}", response_model=CompanyRead)
def remove_company(company_id: int, db: Session = Depends(get_db), current_admin: Admin = Depends(auth_admin_service.get_current_admin)):
    deleted_company = delete_company(db, company_id)
    if not deleted_company:
        raise HTTPException(status_code=404, detail="Company not found")
    return deleted_company
