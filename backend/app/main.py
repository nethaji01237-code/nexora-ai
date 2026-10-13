from app.services.database import get_db_connection
from fastapi import FastAPI
from app.api.documents import router as documents_router
app = FastAPI(
    title="Nexora AI API",
    description="Enterprise Knowledge Intelligence Platform",
    version="0.1.0",
)
app.include_router(documents_router)

@app.get("/")
def root():
    return {
        "application": "Nexora AI",
        "message": "Enterprise Knowledge Intelligence Platform",
        "version": "0.1.0",
    }


@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "healthy",
        "service": "nexora-ai-api",
    }

@app.get("/health/db", tags=["System"])
def database_health_check():
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1;")
                cursor.fetchone()

        return {
            "status": "healthy",
            "database": "connected",
        }

    except Exception:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "database": "disconnected",
            },
        )
