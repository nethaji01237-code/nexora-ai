
from functools import lru_cache

from sentence_transformers import SentenceTransformer


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    """Load the embedding model once and reuse it."""
    return SentenceTransformer(MODEL_NAME)


def generate_embedding(text: str) -> list[float]:
    """Convert one text string into a 384-dimensional vector."""
    if not text.strip():
        raise ValueError("Text cannot be empty")

    model = get_embedding_model()

    embedding = model.encode(
        text,
        normalize_embeddings=True,
    )

    return embedding.tolist()


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """Convert multiple text strings into embeddings."""
    if not texts:
        return []

    if any(not text.strip() for text in texts):
        raise ValueError("Texts cannot contain empty strings")

    model = get_embedding_model()

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        batch_size=32,
        show_progress_bar=False,
    )

    return embeddings.tolist()
