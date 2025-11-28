from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.models.user import User
from app.models.product_transaction import ProductTransaction
from app.schemas.product_transaction import ProductTransactionRead
from app.config.database import get_db
from app.services.auth_user_service import get_current_user

router = APIRouter(tags=["Transactions"])

@router.get("/", response_model=List[ProductTransactionRead])
def get_user_transactions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(ProductTransaction).filter(ProductTransaction.user_id == current_user.id).all()

