
from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.models import Document
from app.services.database import SessionLocal

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.get("/")
def list_documents():
    with SessionLocal() as session:
        documents = session.scalars(
            select(Document).order_by(Document.created_at.desc())
        ).all()

        return [
            {
                "id": document.id,
                "filename": document.filename,
                "status": document.status,
                "created_at": document.created_at,
            }
            for document in documents
        ]


@router.get("/{document_id}")
def get_document(document_id: int):
    with SessionLocal() as session:
        document = session.get(Document, document_id)

        if document is None:
            raise HTTPException(
                status_code=404,
                detail="Document not found",
            )

        return {
            "id": document.id,
            "filename": document.filename,
            "content": document.content,
            "status": document.status,
            "created_at": document.created_at,
        }
