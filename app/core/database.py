from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings

# 1. Creamos el motor de la base de datos usando nuestra URL segura del .env
engine = create_async_engine(settings.DATABASE_URL, echo=False)

# 2. Configuramos la fábrica de sesiones asíncronas
AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# 3. Esta es la función mágica (Dependencia) que usaremos en nuestros endpoints
async def get_db():
    """
    Crea una sesión de base de datos por cada petición de un usuario 
    y la cierra automáticamente cuando termina. ¡Cero fugas de memoria!
    """
    async with AsyncSessionLocal() as session:
        yield session