from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import declarative_base

from app.core.config import settings

Base = declarative_base()

engine = create_async_engine(settings.DATABASE_URL, echo=False)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

async def get_db():
    """
    Crea una sesión de base de datos por cada petición de un usuario 
    y la cierra automáticamente cuando termina. ¡Cero fugas de memoria!
    """
    async with AsyncSessionLocal() as session:
        yield session