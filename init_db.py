import asyncio

from app.core.database import engine
from app.models.user import Base


async def reset_database():
    print("Conectando a PostgreSQL...")
    
    async with engine.begin() as conn:
        print("Borrando tablas viejas (Modo Thanos activado)...")
        # Esto destruye las tablas actuales para no dejar rastro
        await conn.run_sync(Base.metadata.drop_all)
        
        print("Creando las tablas con los nuevos campos...")
        # Esto las vuelve a crear ya con first_name, last_name, etc.
        await conn.run_sync(Base.metadata.create_all)
        
    print("¡Todo listo, pixe! Tu base de datos está actualizada y reluciente.")

if __name__ == "__main__":
    asyncio.run(reset_database())