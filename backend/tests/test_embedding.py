
from app.services.embedding import generate_embedding


def test_embedding_dimensions():
    embedding = generate_embedding("Nexora AI searches enterprise documents.")

    assert len(embedding) == 384


def test_embedding_values_are_finite():
    import math

    embedding = generate_embedding("PostgreSQL stores document chunks.")

    assert all(math.isfinite(value) for value in embedding)


def test_empty_text_is_rejected():
    import pytest

    with pytest.raises(ValueError):
        generate_embedding("   ")
