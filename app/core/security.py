from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

# 1. Configuración de Bcrypt (lo que ya teníamos)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# 2. Nueva lógica de Tokens JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Empaqueta los datos del usuario (como su ID o correo) en un token 
    y lo firma con la SECRET_KEY de tu archivo .env.
    """
    to_encode = data.copy()
    
    # Configuramos el tiempo de expiración (vital para mitigar robos de sesión)
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    # Generamos el token firmado usando el algoritmo definido (HS256)
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt