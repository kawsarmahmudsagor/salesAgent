from pydantic import BaseModel
from typing import List
from admin import AdminRead


class DocumentBase(BaseModel):
    title: str
    summary: str
    tags: str
    uploaded_by_id: int

class DocumentCreate(DocumentBase):
    pass

class DocumentRead(DocumentBase):
    id: int
    uploaded_by: AdminRead
    class Config:
        orm_mode = True