from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.repositories.user import get_user_by_email

# Esto le dice a Swagger dónde está la ruta para conseguir el token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    """
    Este es el filtro mágico. Verifica el token, extrae el correo 
    y te devuelve el usuario completo de la base de datos.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No pudimos validar tus credenciales, papu. Tu token no sirve o expiró.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Intentamos abrir el token con nuestra llave secreta
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    # Si el token es válido, buscamos al usuario en la base de datos
    user = await get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
        
    return user