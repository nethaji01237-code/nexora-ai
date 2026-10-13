
from app.models import Document
from app.services.database import create_tables


if __name__ == "__main__":
    create_tables()
    print("Database tables created successfully.")

    # Confirms the Document model is registered.
    print(f"Registered table: {Document.__tablename__}")
