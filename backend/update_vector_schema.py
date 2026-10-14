
from app.services.database import enable_vector_extension

if __name__ == "__main__":
    enable_vector_extension()
    print("pgvector enabled and embedding column ready.")
