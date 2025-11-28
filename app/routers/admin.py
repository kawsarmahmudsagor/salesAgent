from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.admin import Admin
from app.schemas.admin import AdminRead, AdminCreate
from app.services.auth_admin_service import get_current_admin, get_password_hash
from app.config.database import get_db




router = APIRouter(tags=["Admins"])

@router.post("/", response_model=AdminRead)
def create_admin(admin: AdminCreate, db: Session = Depends(get_db)):

    # Check if email already exists
    db_admin = db.query(Admin).filter(Admin.email == admin.email).first()
    if db_admin:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password
    hashed_password = get_password_hash(admin.password)

    # Create admin with user-supplied role
    new_admin = Admin(
        **admin.dict(exclude={"password"}),
        hashed_password=hashed_password
    )

    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    return new_admin


@router.get("/me", response_model=AdminRead)
def read_current_admin(current_admin: Admin = Depends(get_current_admin)):
    return current_admin