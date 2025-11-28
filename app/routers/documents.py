from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from pathlib import Path
from typing import List
from app.crud.document import get_documents, delete_document, create_document
from app.models.admin import Admin
from app.schemas.document import DocumentCreate, DocumentRead
from app.services import ai_summarizer_service, auth_admin_service
from app.config.database import get_db
import os
import shutil
import uuid

router = APIRouter(tags=["Documents"])

UPLOAD_DIR = Path("Temp-Document-uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.get("/view", response_model=List[DocumentRead])
def view_documents(db: Session = Depends(get_db), current_admin: Admin = Depends(auth_admin_service.get_current_admin)):
    return get_documents(db)

@router.post("/preview", response_model=DocumentCreate)
def preview_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(auth_admin_service.get_current_admin)
):
    # Save uploaded file temporarily
    unique_filename = f"{uuid.uuid4().hex}_{file.filename}"
    temp_file_path = UPLOAD_DIR / unique_filename
    with open(temp_file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        # Generate AI summary and tags
        ai_summary, ai_tags = ai_summarizer_service.tags_generate_summarize_document(temp_file_path)

        # Return DocumentCreate-like object for frontend form
        preview_data = DocumentCreate(
            title=file.filename,
            summary=ai_summary,
            tags=ai_tags,
            uploaded_by_id=current_admin.id
        )
    finally:
        temp_file_path.unlink(missing_ok=True)

    return preview_data

@router.post("/add", response_model=DocumentRead)
def save_document(
    title: str = Form(...),
    summary: str = Form(...),
    tags: str = Form(...),
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(auth_admin_service.get_current_admin)
):
    
    document_data = DocumentCreate(
        title=title,
        summary=summary,  
        tags=tags,        
        uploaded_by_id=current_admin.id
    )
    db_document = create_document(db, document_data)
    return db_document


@router.delete("/delete/{document_id}", response_model=dict)
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(auth_admin_service.get_current_admin)
):
    success = delete_document(db, document_id)
    if not success:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"detail": "Document deleted successfully"}
