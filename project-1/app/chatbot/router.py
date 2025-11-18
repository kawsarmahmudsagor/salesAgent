from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from . import services
from .schemas import ChatRequest, ChatResponse, FeedbackIn, RecommendRequest, FilterQuery
from app.database import get_db
from app.auth import get_current_user

router = APIRouter()

@router.post("/greet")
def greet(user=Depends(get_current_user), db: Session = Depends(get_db)):
    text = services.greet_user(db, user)
    return {"reply": text}

@router.post("/recommend")
def recommend(req: RecommendRequest, db: Session = Depends(get_db)):
    products = services.recommend_products_by_history(db, req.user_id, limit=req.limit)
    return {"products": products}

@router.post("/search")
def search(filters: FilterQuery, db: Session = Depends(get_db)):
    results = services.search_products_with_filters(
        db,
        category=filters.category,
        size=filters.size,
        color=filters.color,
        min_price=filters.min_price,
        max_price=filters.max_price,
        budget=filters.budget,
        limit=filters.limit
    )
    return {"results": results}

@router.get("/discounts")
def discounts(db: Session = Depends(get_db)):
    return {"discounts": services.get_discounts(db)}

@router.post("/feedback")
def feedback(fb: FeedbackIn, db: Session = Depends(get_db)):
    saved = services.save_feedback(db, fb.user_id, fb.product_id, fb.rating, fb.comment)
    return {"feedback": {"id": saved.id, "rating": saved.rating}}

@router.post("/rag")
def rag_query(payload: dict, db: Session = Depends(get_db)):
    q = payload.get("q")
    if not q:
        raise HTTPException(400, "missing q")
    out = services.rag_answer(db, q)
    return out

@router.websocket("/ws/{user_id}")
async def websocket_chat(websocket: WebSocket, user_id: int, db: Session = Depends(get_db)):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            text = data.get("text")
            if not text:
                await websocket.send_json({"reply": "I didn't get your message."})
                continue
            if text.lower().startswith("recommend"):
                prods = services.recommend_products_by_history(db, user_id, limit=5)
                await websocket.send_json({"reply": "Here are recommended products", "products": prods})
                continue
            if text.lower().startswith("discount"):
                discs = services.get_discounts(db, limit=5)
                await websocket.send_json({"reply": "Here are current discounts", "discounts": discs})
                continue
            if text.lower().startswith("policy"):
                out = services.rag_answer(db, text)
                await websocket.send_json({"reply": out["answer"], "sources": out.get("sources")})
                continue
            out = services.rag_answer(db, text)
            await websocket.send_json({"reply": out["answer"]})
    except WebSocketDisconnect:
        return
