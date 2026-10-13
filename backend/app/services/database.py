
import psycopg
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.models import Base


def get_db_connection():
    """Create a PostgreSQL connection using psycopg."""
    return psycopg.connect(settings.database_url)


# SQLAlchemy needs the psycopg 3 driver explicitly specified.
sqlalchemy_url = settings.database_url.replace(
    "postgresql://",
    "postgresql+psycopg://",
    1,
)

engine = create_engine(sqlalchemy_url)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def create_tables():
    Base.metadata.create_all(bind=engine)
