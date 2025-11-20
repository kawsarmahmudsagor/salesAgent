# app/crud.py
from sqlalchemy.orm import Session
from . import models, schemas
from typing import List, Optional

# ----------------- PRODUCTS -----------------
def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_products(
    db: Session, 
    size: Optional[str] = None, 
    color: Optional[str] = None, 
    min_price: float = 0, 
    max_price: float = 1e10, 
    company_id: Optional[int] = None
):
    query = db.query(models.Product)

    # Join inventory only if filtering by size or color
    if size or color:
        query = query.join(models.Inventory)
        if size:
            query = query.filter(models.Inventory.size == size)
        if color:
            query = query.filter(models.Inventory.color == color)

    # Filter by price
    query = query.filter(models.Product.price >= min_price, models.Product.price <= max_price)

    # Filter by company if specified
    if company_id:
        query = query.filter(models.Product.company_id == company_id)

    # Return all products if no filters specified
    return query.all()


def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
    return product

# ----------------- COMPANIES -----------------
def get_company(db: Session, company_id: int):
    return db.query(models.Company).filter(models.Company.id == company_id).first()

def get_companies(db: Session):
    return db.query(models.Company).all()

def create_company(db: Session, company: schemas.CompanyCreate):
    db_company = models.Company(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

def update_company(db: Session, company_id: int, company: schemas.CompanyUpdate):
    db_company = get_company(db, company_id)
    if not db_company:
        return None
    for key, value in company.dict(exclude_unset=True).items():
        setattr(db_company, key, value)
    db.commit()
    db.refresh(db_company)
    return db_company

def delete_company(db: Session, company_id: int):
    db_company = get_company(db, company_id)
    if db_company:
        db.delete(db_company)
        db.commit()
    return db_company

# ----------------- CATEGORIES -----------------
def get_category(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def get_categories(db: Session):
    return db.query(models.Category).all()

def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_category(db: Session, category_id: int, category: schemas.CategoryUpdate):
    db_category = get_category(db, category_id)
    if not db_category:
        return None
    for key, value in category.dict(exclude_unset=True).items():
        setattr(db_category, key, value)
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int):
    db_category = get_category(db, category_id)
    if db_category:
        db.delete(db_category)
        db.commit()
    return db_category

# ----------------- PRODUCT TYPES -----------------
def get_product_type(db: Session, product_type_id: int):
    return db.query(models.ProductType).filter(models.ProductType.id == product_type_id).first()

def get_product_types(db: Session):
    return db.query(models.ProductType).all()

def create_product_type(db: Session, product_type: schemas.ProductTypeCreate):
    db_ptype = models.ProductType(**product_type.dict())
    db.add(db_ptype)
    db.commit()
    db.refresh(db_ptype)
    return db_ptype

def update_product_type(db: Session, product_type_id: int, product_type: schemas.ProductTypeUpdate):
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


# ----------------- CART -----------------
def add_to_cart(db: Session, user_id: int, product_id: int, quantity: int = 1):
    cart_item = models.Cart(user_id=user_id, product_id=product_id, quantity=quantity)
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return cart_item

def get_cart_items(db: Session, user_id: int):
    return db.query(models.Cart).filter(models.Cart.user_id == user_id, models.Cart.status=="active").all()

def delete_cart_item(db: Session, cart_item_id: int):
    item = db.query(models.Cart).filter(models.Cart.id == cart_item_id).first()
    if item:
        db.delete(item)
        db.commit()
    return item

def clear_cart(db: Session, user_id: int):
    db.query(models.Cart).filter(models.Cart.user_id == user_id).delete()
    db.commit()


#-------------Inventory-------------
def create_inventory(db: Session, inventory: schemas.InventoryCreate):
    db_inventory = models.Inventory(**inventory.dict())
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory

def list_inventory_for_product(db: Session, product_id: int) -> List[models.Inventory]:
    return db.query(models.Inventory).filter(models.Inventory.product_id == product_id).all()

def delete_inventory(db: Session, inventory_id: int):
    # Find the inventory item
    inventory = db.query(models.Inventory).filter(models.Inventory.id == inventory_id).first()
    if not inventory:
        return None  # You can raise HTTPException in router if needed

    db.delete(inventory)
    db.commit()
    return inventory

# ----------------- ORDERS -----------------
def create_order(db: Session, user_id: int, user_address: str, items: List[models.Cart]):
    # Calculate total using discounted price
    total_amount = sum([item.product.final_price * item.quantity for item in items])

    # Create the order
    order = models.Order(user_id=user_id, total_amount=total_amount, user_address=user_address)
    db.add(order)
    db.commit()
    db.refresh(order)

    # Add order items
    for item in items:
        order_item = models.OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(order_item)
    db.commit()
    return order


# ----------------- TRANSACTIONS -----------------
def create_transaction(db: Session, user_id: int, order_id: int, trn_amount: float, created_by: str):
    transaction = models.ProductTransaction(
        user_id=user_id,
        order_id=order_id,
        trn_type=models.TrnTypeEnum.payment,
        trn_amount=trn_amount,
        credit_amount=trn_amount,
        debit_amount=0,
        created_by=created_by
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction
