from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi import Query

from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User,Role
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

def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Valida que el usuario no esté 'borrado' o suspendido."""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario inactivo o suspendido"
        )
    return current_user

def get_current_admin(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """Valida que el usuario sea administrador (Superuser)."""
    if current_user.role != Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Requiere rol de Administrador"
        )

    return current_user

def get_current_teacher(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """Cadenero nivel 2: Deja pasar a Profesores y Administradores."""
    # Si su rol NO es Admin NI Profesor, lo rebotamos
    if current_user.role not in [Role.ADMIN, Role.TEACHER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Requiere rol de Profesor"
        )
    return current_user

def get_pagination_params(
    skip: int = Query(0, ge=0, description="Cuántos registros saltar (Offset)"),
    limit: int = Query(10, ge=1, le=100, description="Límite máximo por página (Max 100)")
) -> dict:
    """
    Dependencia global para estandarizar la paginación en toda la API.
    Devuelve un diccionario
    """
    return {"skip": skip, "limit": limit}