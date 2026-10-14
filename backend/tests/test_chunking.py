
import pytest

from app.services.chunking import split_text


def test_empty_text_returns_no_chunks():
    assert split_text("") == []


def test_short_text_returns_one_chunk():
    assert split_text("Hello Nexora") == ["Hello Nexora"]


def test_long_text_is_split():
    text = "a" * 1000

    chunks = split_text(text, chunk_size=500, overlap=100)

    assert len(chunks) == 3
    assert all(len(chunk) <= 500 for chunk in chunks)


def test_chunks_overlap():
    text = "abcdefghijklmnopqrstuvwxyz"

    chunks = split_text(text, chunk_size=10, overlap=3)

    assert chunks[0][-3:] == chunks[1][:3]


def test_invalid_chunk_size_is_rejected():
    with pytest.raises(ValueError):
        split_text("hello", chunk_size=0)


def test_invalid_overlap_is_rejected():
    with pytest.raises(ValueError):
        split_text("hello", chunk_size=10, overlap=10)
