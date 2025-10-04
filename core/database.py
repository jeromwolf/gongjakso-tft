"""
Database Configuration and Session Management
"""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator
from loguru import logger

from .config import settings


# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # SQL 로그 출력 (개발 모드)
    pool_pre_ping=True,   # 연결 상태 확인
    pool_size=10,         # 커넥션 풀 크기
    max_overflow=20       # 최대 추가 연결 수
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)


# Base class for all models
class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models"""
    pass


# Dependency for FastAPI routes
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Database session dependency for FastAPI routes

    Usage:
        @app.get("/items")
        async def get_items(db: AsyncSession = Depends(get_db)):
            result = await db.execute(select(Item))
            return result.scalars().all()
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            await session.close()


async def create_all_tables():
    """
    Create all database tables

    Usage:
        await create_all_tables()
    """
    async with engine.begin() as conn:
        logger.info("Creating database tables...")
        await conn.run_sync(Base.metadata.create_all)
        logger.success(f"Tables created: {list(Base.metadata.tables.keys())}")


async def drop_all_tables():
    """
    Drop all database tables (USE WITH CAUTION!)

    Usage:
        await drop_all_tables()
    """
    async with engine.begin() as conn:
        logger.warning("Dropping all database tables...")
        await conn.run_sync(Base.metadata.drop_all)
        logger.success("All tables dropped")
