# app/main.py
from fastapi import FastAPI
from .database import engine
from . import models
from .routers import users, products, inventory, cart, orders, transactions

# create tables (use migrations like Alembic in production)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-Commerce FastAPI")

# Routers
app.include_router(users.router, prefix="", tags=["auth"])
app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(inventory.router, prefix="/inventory", tags=["inventory"])
app.include_router(cart.router, prefix="/cart", tags=["cart"])
app.include_router(orders.router, prefix="/orders", tags=["orders"])
app.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
