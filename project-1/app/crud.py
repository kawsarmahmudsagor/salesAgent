# app/crud.py
from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas
from .auth import get_password_hash
from sqlalchemy import and_, or_, func
from .auth import verify_password

# ---------------- USERS ----------------
def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user_in: schemas.UserCreate) -> models.User:
    hashed = get_password_hash(user_in.password)
    user = models.User(
        email=user_in.email,
        hashed_password=hashed,
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        address=user_in.address,
        contact_no=user_in.contact_no,
        picture=user_in.picture or None
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    # create an empty cart for user
    cart = models.Cart(user_id=user.id)
    db.add(cart)
    db.commit()
    return user

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

# ---------------- PRODUCTS ----------------
def create_product(db: Session, product_in: schemas.ProductCreate) -> models.Product:
    product = models.Product(
        name=product_in.name,
        details=product_in.details,
        price=product_in.price,
        picture=product_in.picture,
        company_id=product_in.company_id,
        product_type_id=product_in.product_type_id,
        category_id=product_in.category_id
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def get_product(db: Session, product_id: int) -> Optional[models.Product]:
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def delete_product(db: Session, product_id: int) -> bool:
    product = get_product(db, product_id)
    if not product:
        return False
    db.delete(product)
    db.commit()
    return True

def list_products(db: Session,
                  size: Optional[str] = None,
                  color: Optional[str] = None,
                  min_price: Optional[float] = None,
                  max_price: Optional[float] = None,
                  skip: int = 0, limit: int = 50) -> List[models.Product]:
    product = db.query(models.Product)
    # If filtering by inventory attributes (size/color), join Inventory
    if size or color:
        product = product.join(models.Inventory)
        if size:
            product = product.filter(models.Inventory.size == size)
        if color:
            product = product.filter(models.Inventory.color == color)
    if min_price is not None:
        product = product.filter(models.Product.price >= min_price)
    if max_price is not None:
        product = product.filter(models.Product.price <= max_price)
    product = product.distinct().offset(skip).limit(limit)
    return product.all()

# ---------------- INVENTORY ----------------
def create_inventory(db: Session, inventory_in: schemas.InventoryCreate) -> models.Inventory:
    inventory = models.Inventory(
        product_id=inventory_in.product_id,
        color=inventory_in.color,
        size=inventory_in.size,
        quantity=inventory_in.quantity
    )
    db.add(inventory)
    db.commit()
    db.refresh(inventory)
    return inventory

def list_of_inventory_for_product(db: Session, product_id: int) -> List[models.Inventory]:
    return db.query(models.Inventory).filter(models.Inventory.product_id == product_id).all()

# ---------------- CART ----------------
def get_cart_by_user(db: Session, user_id: int) -> Optional[models.Cart]:
    return db.query(models.Cart).filter(models.Cart.user_id == user_id).first()

def add_to_cart(db: Session, user_id: int, product_id: int, quantity: int = 1) -> models.CartItem:
    cart = get_cart_by_user(db, user_id)
    if not cart:
        cart = models.Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    # if same product exists in cart, increase quantity
    existing_item = db.query(models.CartItem).filter(
        models.CartItem.cart_id == cart.id,
        models.CartItem.product_id == product_id
    ).first()
    if existing_item:
        existing_item.quantity = existing_item.quantity + quantity
        existing_item.status = "active"
        db.add(existing_item)
        db.commit()
        db.refresh(existing_item)
        return existing_item
    item = models.CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity, status="active")
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def remove_cart_item(db: Session, cart_item_id: int) -> bool:
    item = db.query(models.CartItem).filter(models.CartItem.id == cart_item_id).first()
    if not item:
        return False
    db.delete(item)
    db.commit()
    return True

def clear_cart(db: Session, cart_id: int):
    db.query(models.CartItem).filter(models.CartItem.cart_id == cart_id).delete()
    db.commit()

def delete_cart(db: Session, cart_id: int) -> bool:
    cart = db.query(models.Cart).filter(models.Cart.id == cart_id).first()
    if not cart:
        return False
    # delete items (cascade might already handle)
    db.query(models.CartItem).filter(models.CartItem.cart_id == cart_id).delete()
    db.delete(cart)
    db.commit()
    return True

# ---------------- ORDERS & CHECKOUT ----------------
def checkout_cart(db: Session, user: models.User, user_address: str):
    """
    Create an order from current user's cart items and return created order.
    This function simulates payment as successful. After creating order and transaction,
    it deletes the cart items.
    """
    cart = get_cart_by_user(db, user.id)
    if not cart:
        raise ValueError("Cart not found")
    items = db.query(models.CartItem).filter(models.CartItem.cart_id == cart.id).all()
    if not items:
        raise ValueError("Cart is empty")
    total = 0.0
    # compute total and ensure products exist
    product_map = {}
    for item in items:
        product = get_product(db, item.product_id)
        if not product:
            raise ValueError(f"Product id {item.product_id} not found")
        total += float(product.price) * int(item.quantity)
        product_map[item.product_id] = product

    # create order
    order = models.Order(user_id=user.id, total_amount=total, user_address=user_address)
    db.add(order)
    db.commit()
    db.refresh(order)

    # create order items
    for item in items:
        order_items = models.OrderItem(order_id=order.id, product_id=item.product_id, quantity=item.quantity)
        db.add(order_items)
    db.commit()

    # simulate payment success => create transaction
    trn = models.ProductTransaction(
        order_id=order.id,
        user_id=user.id,
        trn_type=models.TrnTypeEnum.payment,
        trn_amount=total,
        credit_amount=total,
        debit_amount=0.0,
        payment_gateway_trn_id=f"SIM-{order.id}",
        payment_method="simulated",
        created_by=f"user:{user.id}"
    )
    db.add(trn)
    db.commit()
    db.refresh(trn)

    # after successful payment remove cart items
    clear_cart(db, cart.id)

    return order, trn

# ---------------- TRANSACTIONS ----------------
def list_transactions_for_user(db: Session, user_id: int):
    return db.query(models.ProductTransaction).filter(models.ProductTransaction.user_id == user_id).order_by(models.ProductTransaction.created_at.desc()).all()

# ---------------- ORDERS ----------------
def get_orders_for_user(db: Session, user_id: int):
    return db.query(models.Order).filter(models.Order.user_id == user_id).order_by(models.Order.created_at.desc()).all()

def get_order(db: Session, order_id: int) -> Optional[models.Order]:
    return db.query(models.Order).filter(models.Order.id == order_id).first()
