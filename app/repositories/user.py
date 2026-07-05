import uuid

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.security import get_password_hash
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


async def get_user_by_email(db: AsyncSession, email: str):
    """
    Busca un usuario por su correo. 
    Crucial para verificar si alguien ya existe o para el login.
    """
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()

async def get_users_count(db: AsyncSession) -> int:
    """
    Cuenta cuántos usuarios existen en total en la base de datos.
    Crucial para calcular la metadata de la paginación.
    """
    result = await db.execute(select(func.count()).select_from(User))
    return result.scalar()

async def get_all_users_paginated(db: AsyncSession, skip: int = 0, limit: int = 10):
    """
    Trae la lista de usuarios en rebanadas para no saturar la memoria (Paginación).
    """
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()

async def get_user_by_id(db: AsyncSession, user_id: uuid.UUID):
    """
    Busca a un usuario por su ID único.
    """
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalars().first()

# ==========================================
# FUNCIONES DE ESCRITURA (POST, PUT, DELETE)
# ==========================================

async def create_user(db: AsyncSession, user: UserCreate):
    """
    Toma los datos de Pydantic, encripta la contraseña y guarda al usuario.
    """
    hashed_password = get_password_hash(user.password)
    
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
    update_data = user_in.model_dump(exclude_unset=True)
    
    if "password" in update_data:
        hashed_password = get_password_hash(update_data["password"])
        db_user.hashed_password = hashed_password
        del update_data["password"] 
    
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
    db_user.is_active = False

    db.add(db_user)

    await db.commit()
    await db.refresh(db_user)
    return db_user