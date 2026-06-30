import asyncio
from sqlalchemy.future import select
from app.core.database import get_db
from app.models.user import User, Role

async def fix_old_users():
    async for db in get_db():
        # 1. Buscamos a todos los usuarios que tienen el rol vacío (NULL)
        result = await db.execute(select(User).filter(User.role == None))
        old_users = result.scalars().all()
        
        # 2. Les asignamos el rol de estudiante por defecto
        for user in old_users:
            user.role = Role.STUDENT
            
        # 3. Guardamos los cambios
        await db.commit()
        print(f"✅ ¡Chopiadito! Se arreglaron {len(old_users)} usuarios veteranos.")
        break

if __name__ == "__main__":
    asyncio.run(fix_old_users())