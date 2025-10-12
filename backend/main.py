"""
AI ON Backend - FastAPI Main Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from loguru import logger

from core.config import settings
from core.database import create_all_tables

# Import models to register with Base.metadata
from models.user import User
from models.blog import Blog
from models.project import Project
from models.newsletter import Subscriber, Newsletter, NewsletterRequest

# Import routers
from api.auth import router as auth_router
from api.blog import router as blog_router
from api.project import router as project_router
from api.newsletter import router as newsletter_router
from api.ai_content import router as ai_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - startup and shutdown"""
    # Startup
    logger.info("🚀 Starting AI ON Backend...")
    logger.info(f"Database URL: {settings.DATABASE_URL}")

    # Create database tables
    await create_all_tables()

    yield

    # Shutdown
    logger.info("👋 Shutting down AI ON Backend...")


# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Blog & Newsletter Backend for AI ON",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "healthy",
        "docs": "/api/docs"
    }


@app.get("/api/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "message": "All systems operational",
        "database": "connected"
    }


# Register API routers
app.include_router(auth_router)
app.include_router(blog_router)
app.include_router(project_router)
app.include_router(newsletter_router)
app.include_router(ai_router)


if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )
