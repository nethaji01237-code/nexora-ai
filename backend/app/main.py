
from fastapi import FastAPI

app = FastAPI(
    title="Nexora AI API",
    description="Enterprise Knowledge Intelligence Platform",
    version="0.1.0",
)


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
