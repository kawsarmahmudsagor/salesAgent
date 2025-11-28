from sqlalchemy.orm import Session
from app.models.inventory import Inventory
from app.schemas.inventory import InventoryCreate
from typing import List, Optional

def create_inventory(db: Session, inventory: InventoryCreate):
    db_inventory = Inventory(**inventory.dict())
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory

def list_inventory_for_product(db: Session, product_id: int) -> List[Inventory]:
    return db.query(Inventory).filter(Inventory.product_id == product_id).all()

def delete_inventory(db: Session, inventory_id: int):
    # Find the inventory item
    inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not inventory:
        return None  # You can raise HTTPException in router if needed

    db.delete(inventory)
    db.commit()
    return inventory