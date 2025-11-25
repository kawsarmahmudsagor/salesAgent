from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(tags=["Admins"])

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(tags=["Admins"])

@router.post("/", response_model=schemas.AdminRead)
def create_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db)):

    # Check if email already exists
    db_admin = db.query(models.Admin).filter(models.Admin.email == admin.email).first()
    if db_admin:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password
    hashed_password = auth.get_password_hash(admin.password)

    # Create admin with user-supplied role
    new_admin = models.Admin(
        **admin.dict(exclude={"password"}),
        hashed_password=hashed_password
    )

    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    return new_admin


@router.get("/me", response_model=schemas.AdminRead)
def read_current_admin(current_admin: models.Admin = Depends(auth.get_current_admin)):
    return current_admin