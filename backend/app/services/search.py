
from sqlalchemy import select

from app.models import DocumentChunk
from app.services.database import SessionLocal
from app.services.embedding import generate_embedding


def search_chunks(query: str, limit: int = 5) -> list[dict]:
    """Find document chunks semantically similar to a query."""

    if not query.strip():
        raise ValueError("Search query cannot be empty")

    if not 1 <= limit <= 20:
        raise ValueError("limit must be between 1 and 20")

    query_embedding = generate_embedding(query)

    with SessionLocal() as session:
        distance = DocumentChunk.embedding.cosine_distance(
            query_embedding
        ).label("distance")

        statement = (
            select(DocumentChunk, distance)
            .where(DocumentChunk.embedding.is_not(None))
            .order_by(distance)
            .limit(limit)
        )

        results = session.execute(statement).all()

        return [
            {
                "chunk_id": chunk.id,
                "document_id": chunk.document_id,
                "chunk_index": chunk.chunk_index,
                "content": chunk.content,
                "similarity": round(1 - distance_value, 4),
            }
            for chunk, distance_value in results
        ]
