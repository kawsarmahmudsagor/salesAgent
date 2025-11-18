from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ChatRequest(BaseModel):
    user_id: int
    text: str
    context: Optional[dict] = None

class ChatResponse(BaseModel):
    user_id: int
    reply: str
    sources: Optional[List[str]] = None

class FeedbackIn(BaseModel):
    user_id: int
    product_id: int
    rating: int
    comment: Optional[str] = None

class FeedbackOut(FeedbackIn):
    id: int
    created_at: datetime

class RecommendRequest(BaseModel):
    user_id: int
    limit: Optional[int] = 5

class FilterQuery(BaseModel):
    user_id: int
    category: Optional[str] = None
    size: Optional[str] = None
    color: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    budget: Optional[float] = None
    limit: Optional[int] = 10
