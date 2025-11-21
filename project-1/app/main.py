from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .database import engine
from . import models
from .routers import (
    companies,
    users,
    categories,
    product_types,
    products,
    inventory,
    cart,
    orders,
    transactions,
    auth,
    chatbot_route,
)


# Create tables (use Alembic for production migrations)
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
api = FastAPI(title="E-Commerce FastAPI")

# Include routers
api.include_router(companies.router, prefix="/companies", tags=["Companies"])
api.include_router(users.router, prefix="/users", tags=["Users"])
api.include_router(categories.router, prefix="/categories", tags=["Categories"])
api.include_router(product_types.router, prefix="/product_types", tags=["Product-Types"])
api.include_router(products.router, prefix="/products", tags=["Products"])
api.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])
api.include_router(cart.router, prefix="/cart", tags=["Cart"])
api.include_router(orders.router, prefix="/orders", tags=["Orders"])
api.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])
api.include_router(auth.router, prefix="/auth", tags=["Auth"])
api.include_router(chatbot_route.router, prefix="/chatbot", tags=["Chatbot"])


# Mount uploads folder for serving static files
api.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
