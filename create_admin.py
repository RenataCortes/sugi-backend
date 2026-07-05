import asyncio

from sqlalchemy.future import select

# Importamos las herramientas de tu proyecto
from app.core.database import get_db
from app.core.security import get_password_hash
from app.models.user import Role, User


async def create_super_admin():
    # Extraemos una sesión de tu base de datos manualmente
    async for db in get_db():
        email_admin = "admin@sugi.com"
        
        # 1. Revisamos si ya lo habías creado antes para no duplicarlo
        result = await db.execute(select(User).filter(User.email == email_admin))
        existing_user = result.scalars().first()
        
        if existing_user:
            print("⚠️ El administrador ya existe, papu.")
            return

        # 2. Fabricamos al dueño del antro
        hashed_pwd = get_password_hash("Admin123!") # <-- Contraseña temporal
        
        admin_user = User(
            first_name="Super",
            last_name="Admin",
            email=email_admin,
            hashed_password=hashed_pwd,
            role=Role.ADMIN,
            is_active=True
        )
        
        db.add(admin_user)
        await db.commit()
        print("✅ ¡Primer Administrador creado con éxito! Las llaves son tuyas.")
        
        break # Terminamos y cerramos la conexión

if __name__ == "__main__":
    asyncio.run(create_super_admin())