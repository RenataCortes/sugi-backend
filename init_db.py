import asyncio
import os
import selectors

from dotenv import load_dotenv
from sqlalchemy.future import select

from app.core.database import engine, get_db
from app.core.security import get_password_hash
from app.models.user import Base, Role, User

load_dotenv()

async def reset_database():
    print("Conectando a PostgreSQL...")
    
    async with engine.begin() as conn:
        print("Borrando tablas viejas...")
        # Esto destruye las tablas actuales para no dejar rastro
        await conn.run_sync(Base.metadata.drop_all)
        
        print("Creando las tablas con los nuevos campos...")
        # Esto las vuelve a crear ya con first_name, last_name, etc.
        await conn.run_sync(Base.metadata.create_all)
        
    print("La base de datos está actualizada.")

async def create_super_admin():
    async for db in get_db():
        email_admin = "admin@sugi.com"
        
        # Leer la contraseña desde el entorno
        admin_pwd = os.getenv("ADMIN_PASSWORD", "DefaultPassword123!")
        
        result = await db.execute(select(User).filter(User.email == email_admin))
        if result.scalars().first():
            print("⚠️ El administrador ya existe.")
            return

        admin_user = User(
            first_name="Super",
            last_name="Admin",
            email=email_admin,
            hashed_password=get_password_hash(admin_pwd),
            role=Role.ADMIN,
            is_active=True
        )
        db.add(admin_user)
        await db.commit()
        print("¡Administrador inicial creado de forma segura!")
        break

async def init_system():
    await reset_database()
    await create_super_admin()

if __name__ == "__main__":
    selector = selectors.SelectSelector()
    loop = asyncio.SelectorEventLoop(selector)
    asyncio.set_event_loop(loop)
    
    try:
        loop.run_until_complete(init_system())
    finally:
        loop.close()