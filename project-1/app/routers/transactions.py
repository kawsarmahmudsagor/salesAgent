# app/routers/transactions.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud, models
from ..database import get_db
from ..auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[schemas.ProductTransactionRead])
def list_my_transactions(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.list_transactions_for_user(db, current_user.id)
