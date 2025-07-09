from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.infrastructure.config.settings import settings

# Создаем async engine
engine = create_async_engine(settings.database_url, echo=True)

# Создаем async session factory
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_session() -> AsyncSession:
    """Dependency для получения AsyncSession."""
    async with AsyncSessionLocal() as session:
        yield session
