from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.schemas.user import UserCreate
from app.repositories.user import get_user_by_email, create_user
from app.core.security import verify_password, create_access_token

async def register_new_user(db: AsyncSession, user_data: UserCreate):
    """
    Lógica de negocio para registrar a un usuario.
    Revisa que no exista y luego lo manda a guardar.
    """
    existing_user = await get_user_by_email(db, email=user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este correo electrónico ya está registrado en el sistema."
        )
    
    return await create_user(db, user=user_data)

async def authenticate_user(db: AsyncSession, email: str, password: str):
    """
    Lógica de negocio para el login.
    Valida credenciales y escupe el token.
    """
    user = await get_user_by_email(db, email=email)
    
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos, papu",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}