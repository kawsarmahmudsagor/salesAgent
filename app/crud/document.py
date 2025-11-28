from sqlalchemy.orm import Session
from app.models.documents import Document
from app.schemas.document import DocumentCreate
from typing import List


def get_documents(db: Session)->List[Document]:
    return db.query(Document).all()

def create_document(db: Session, document: DocumentCreate) -> Document:
    db_document = Document(
        title=document.title,              
        summary=document.summary,
        tags=document.tags,
        uploaded_by_id=document.uploaded_by_id 
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

def delete_document(db: Session, document_id: int) -> bool:
    db_document = db.query(Document).filter(Document.id == document_id).first()
    if not db_document:
        return False
    db.delete(db_document)
    db.commit()
    return True