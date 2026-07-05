from datetime import datetime, timedelta
from typing import Optional

import bcrypt
from jose import jwt

from app.core.config import settings


# 1. Configuración de Bcrypt (Nativa y segura)
def get_password_hash(password: str) -> str:
    # Truncamos a 72 bytes para evitar errores de bcrypt y hasheamos
    pwd_bytes = password.encode('utf-8')[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Verificamos la contraseña truncándola también a 72 bytes por seguridad
    pwd_bytes = plain_password.encode('utf-8')[:72]
    hash_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(pwd_bytes, hash_bytes)

# 2. Lógica de Tokens JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Empaqueta los datos del usuario en un token y lo firma con la SECRET_KEY.
    """
    to_encode = data.copy()
    
    # Configuración de tiempo de expiración
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    # Generación del token
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt