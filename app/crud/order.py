from sqlalchemy.orm import Session
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.cart import Cart
from typing import List, Optional


def create_order(db: Session, user_id: int, user_address: str, items: List[Cart]) -> Order:
    # Calculate total using discounted price
    total_amount = sum([item.product.final_price * item.quantity for item in items])

    # Create the order
    order = Order(user_id=user_id, total_amount=total_amount, user_address=user_address)
    db.add(order)
    db.commit()
    db.refresh(order)

    # Add order items
    for item in items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(order_item)
    db.commit()
    return order