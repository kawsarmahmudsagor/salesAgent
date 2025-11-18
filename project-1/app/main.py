# app/main.py
from fastapi import FastAPI
from .database import engine
from . import models
from .routers import users, products, inventory, cart, orders, transactions, auth
from app.chatbot.router import router as chatbot_router

# create tables (use migrations like Alembic in production)
models.Base.metadata.create_all(bind=engine)

api = FastAPI(title="E-Commerce FastAPI")

# Routers
api.include_router(users.router, prefix="/users", tags=["Users"])
api.include_router(products.router, prefix="/products", tags=["products"])
api.include_router(inventory.router, prefix="/inventory", tags=["inventory"])
api.include_router(cart.router, prefix="/cart", tags=["cart"])
api.include_router(orders.router, prefix="/orders", tags=["orders"])
api.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
api.include_router(auth.router, prefix="/auth", tags=["auth"])
api.include_router(chatbot_router, prefix="/chatbot", tags=["chatbot"])