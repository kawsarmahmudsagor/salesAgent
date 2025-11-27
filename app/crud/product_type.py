from sqlalchemy.orm import Session
from models.product_type import ProductType
from schemas.product_type import ProductTypeCreate, ProductTypeUpdate
from typing import List, Optional

def get_product_type(db: Session, product_type_id: int):
    return db.query(ProductType).filter(ProductType.id == product_type_id).first()

def get_product_types(db: Session):
    return db.query(ProductType).all()

def create_product_type(db: Session, product_type: ProductTypeCreate):
    db_ptype = ProductType(**product_type.dict())
    db.add(db_ptype)
    db.commit()
    db.refresh(db_ptype)
    return db_ptype

def update_product_type(db: Session, product_type_id: int, product_type: ProductTypeUpdate):
    db_ptype = get_product_type(db, product_type_id)
    if not db_ptype:
        return None
    for key, value in product_type.dict(exclude_unset=True).items():
        setattr(db_ptype, key, value)
    db.commit()
    db.refresh(db_ptype)
    return db_ptype

def delete_product_type(db: Session, product_type_id: int):
    db_ptype = get_product_type(db, product_type_id)
    if db_ptype:
        db.delete(db_ptype)
        db.commit()
    return db_ptype