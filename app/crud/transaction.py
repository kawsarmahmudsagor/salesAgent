from sqlalchemy.orm import Session
from models.product_transaction import ProductTransaction
from schemas.transaction_type import TrnTypeEnum
from typing import List, Optional

def create_transaction(db: Session, user_id: int, order_id: int, trn_amount: float, created_by: str):
    transaction = ProductTransaction(
        user_id=user_id,
        order_id=order_id,
        trn_type=TrnTypeEnum.payment,
        trn_amount=trn_amount,
        credit_amount=trn_amount,
        debit_amount=0,
        created_by=created_by
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction