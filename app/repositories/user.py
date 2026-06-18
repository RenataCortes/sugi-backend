from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import UserCreate
from app.schemas.user import UserUpdate
from app.core.security import get_password_hash

async def get_user_by_email(db: AsyncSession, email: str):
    """
    Busca un usuario por su correo. 
    Crucial para verificar si alguien ya existe o para el login.
    """
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()

async def create_user(db: AsyncSession, user: UserCreate):
    """
    Toma los datos de Pydantic, encripta la contraseña y guarda al usuario.
    """
    hashed_password = get_password_hash(user.password)
    
    # Pasamos los nuevos campos obligatorios
    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        hashed_password=hashed_password
    )
    
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    
    return db_user
async def update_user(db: AsyncSession, db_user: User, user_in: UserUpdate):
    """
    Actualiza los datos del usuario. Si manda password, la encripta de nuevo.
    """
    # Convertimos los datos que mandó a un diccionario, ignorando lo que no envió
    update_data = user_in.model_dump(exclude_unset=True)
    
    # Si quiere cambiar la contraseña, la tenemos que hashear otra vez
    if "password" in update_data:
        hashed_password = get_password_hash(update_data["password"])
        db_user.hashed_password = hashed_password
        del update_data["password"] # Borramos la de texto plano
    
    # Actualizamos el resto de los campos
    for field, value in update_data.items():
        setattr(db_user, field, value)
        
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def delete_user(db: AsyncSession, db_user: User):
    """
    Elimina al usuario de la base de datos para siempre.
    """
    await db.delete(db_user)
    await db.commit()
    return db_user