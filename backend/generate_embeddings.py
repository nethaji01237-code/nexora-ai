
from sqlalchemy import select

from app.models import DocumentChunk
from app.services.database import SessionLocal
from app.services.embedding import generate_embeddings


BATCH_SIZE = 32


def populate_embeddings():
    total_processed = 0

    while True:
        with SessionLocal() as session:
            chunks = session.scalars(
                select(DocumentChunk)
                .where(DocumentChunk.embedding.is_(None))
                .order_by(DocumentChunk.id)
                .limit(BATCH_SIZE)
            ).all()

            if not chunks:
                break

            # Keep the IDs and text before generating embeddings.
            chunk_data = [
                (chunk.id, chunk.content)
                for chunk in chunks
            ]

            vectors = generate_embeddings(
                [content for _, content in chunk_data]
            )

            for (chunk_id, _), vector in zip(chunk_data, vectors):
                chunk = session.get(DocumentChunk, chunk_id)
                chunk.embedding = vector

            session.commit()
            total_processed += len(chunk_data)

            print(f"Embedded {total_processed} chunks...")

    print(f"Finished. Total chunks embedded: {total_processed}")


if __name__ == "__main__":
    populate_embeddings()
