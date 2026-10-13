
from app.services.database import get_db_connection


def test_database_connection():
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            result = cursor.fetchone()

            print("Database connection successful!")
            print(result[0])


if __name__ == "__main__":
    test_database_connection()
