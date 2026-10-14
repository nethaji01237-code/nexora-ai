from app.models import DocumentChunk
from app.services.chunking import split_text
from app.services.search import search_chunks

from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile, File
from pypdf import PdfReader
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
@router.get("/search")
def search_documents(q: str, limit: int = 5):
    try:
        results = search_chunks(q, limit)
        return {
            "query": q,
            "results": results,
            "count": len(results),
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

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


@router.post("/upload", status_code=201)
def upload_document(file: UploadFile = File(...)):
    if Path(file.filename or "").suffix.lower() != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    try:
        reader = PdfReader(file.file)

        if reader.is_encrypted:
            raise HTTPException(
                status_code=400,
                detail="Encrypted PDFs are not supported.",
            )

        content = "\n".join(
            page.extract_text() or "" for page in reader.pages
        ).strip()

        if not content:
            raise HTTPException(
                status_code=400,
                detail="No extractable text found in the PDF.",
            )

        chunks = split_text(content, chunk_size=500, overlap=100)

        with SessionLocal() as session:
            document = Document(
                filename=Path(file.filename).name,
                content=content,
                status="processed",
            )

            session.add(document)
            session.flush()  # Obtain the document ID before saving chunks.

            for index, chunk_content in enumerate(chunks):
                session.add(
                    DocumentChunk(
                        document_id=document.id,
                        chunk_index=index,
                        content=chunk_content,
                    )
                )

            session.commit()
            session.refresh(document)

            return {
                "id": document.id,
                "filename": document.filename,
                "status": document.status,
                "characters_extracted": len(content),
                "chunks_created": len(chunks),
                "message": "PDF uploaded and chunked successfully.",
            }

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Unable to process this PDF.",
        )
    finally:
        file.file.close()


