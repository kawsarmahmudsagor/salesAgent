from .models import ChatMessage, Feedback
from .rag_index import keyword_search_policy, generate_embedding_google, embedding_retrieve
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import json

def greet_user(db: Session, user):
    name = getattr(user, "full_name", None) or getattr(user, "name", None) or "there"
    text = f"Hi {name}! 👋 Welcome back. I can suggest shoes you might like, tell you about discounts, or help with orders. What would you like today?"
    db.add(ChatMessage(user_id=user.id, role="bot", message=text, created_at=datetime.utcnow()))
    db.commit()
    return text

def recommend_products_by_history(db: Session, user_id: int, limit: int = 5):
    sql = """
    SELECT p.id, p.title, p.price, p.discount, p.stock
    FROM products p
    JOIN (
      SELECT oi.product_id, COUNT(*) as cnt
      FROM order_items oi
      JOIN orders o ON oi.order_id = o.id
      WHERE o.user_id = :user_id
      GROUP BY oi.product_id
      ORDER BY cnt DESC
      LIMIT 5
    ) rec ON rec.product_id = p.id
    LIMIT :lim
    """
    try:
        rows = db.execute(sql, {"user_id": user_id, "lim": limit}).fetchall()
        products = [dict(id=r[0], title=r[1], price=r[2], discount=r[3], stock=r[4]) for r in rows]
    except Exception:
        rows = db.execute("SELECT id, title, price, discount, stock FROM products ORDER BY discount DESC LIMIT :lim", {"lim": limit}).fetchall()
        products = [dict(id=r[0], title=r[1], price=r[2], discount=r[3], stock=r[4]) for r in rows]
    return products

def search_products_with_filters(db: Session, *,
                                 category: Optional[str] = None,
                                 size: Optional[str] = None,
                                 color: Optional[str] = None,
                                 min_price: Optional[float] = None,
                                 max_price: Optional[float] = None,
                                 budget: Optional[float] = None,
                                 limit: int = 10):
    where = []
    params = {}
    if category:
        where.append("category = :category")
        params["category"] = category
    if size:
        where.append("size = :size")
        params["size"] = size
    if color:
        where.append("color = :color")
        params["color"] = color
    if min_price is not None:
        where.append("price >= :min_price")
        params["min_price"] = min_price
    if max_price is not None:
        where.append("price <= :max_price")
        params["max_price"] = max_price
    if budget is not None:
        where.append("price <= :budget")
        params["budget"] = budget

    where_sql = " AND ".join(where) if where else "1=1"
    sql = f"SELECT id, title, price, discount, stock FROM products WHERE {where_sql} ORDER BY discount DESC LIMIT :lim"
    params["lim"] = limit
    rows = db.execute(sql, params).fetchall()
    return [dict(id=r[0], title=r[1], price=r[2], discount=r[3], stock=r[4]) for r in rows]

def get_discounts(db: Session, limit: int = 10):
    rows = db.execute("SELECT id, title, price, discount FROM products WHERE discount > 0 ORDER BY discount DESC LIMIT :lim", {"lim": limit}).fetchall()
    return [dict(id=r[0], title=r[1], price=r[2], discount=r[3]) for r in rows]

def ask_feedback_on_past_purchases(db: Session, user_id: int, limit: int = 3):
    sql = """
    SELECT p.id, p.title
    FROM products p
    JOIN order_items oi ON p.id = oi.product_id
    JOIN orders o ON oi.order_id = o.id
    WHERE o.user_id = :user_id
    ORDER BY o.created_at DESC
    LIMIT :lim
    """
    rows = db.execute(sql, {"user_id": user_id, "lim": limit}).fetchall()
    items = [dict(id=r[0], title=r[1]) for r in rows]
    if not items:
        return None
    prompt = "You recently bought: " + ", ".join([it["title"] for it in items]) + ". Would you like to leave feedback for any of these?"
    return {"items": items, "prompt": prompt}

def save_feedback(db: Session, user_id: int, product_id: int, rating: int, comment: str = None):
    fb = Feedback(user_id=user_id, product_id=product_id, rating=rating, comment=comment, created_at=datetime.utcnow())
    db.add(fb)
    db.commit()
    db.refresh(fb)
    return fb

def rag_answer(db: Session, query: str, use_google_embeddings: bool = True):
    if use_google_embeddings:
        emb = generate_embedding_google(query)
        if emb:
            try:
                docs = embedding_retrieve(db, emb, top_k=3)
            except Exception:
                docs = keyword_search_policy(db, query, limit=3)
        else:
            docs = keyword_search_policy(db, query, limit=3)
    else:
        docs = keyword_search_policy(db, query, limit=3)
    snippets = [d[2][:800] for d in docs]
    answer = "".join([s + "\n\n" for s in snippets])
    if not answer.strip():
        answer = "I couldn't find a policy about that exact phrase. Please refer to our general return and refund policy."
    return {"answer": answer, "sources": [d[1] for d in docs]}
