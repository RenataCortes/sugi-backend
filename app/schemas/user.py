from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import uuid

# 1. Lo que el usuario nos manda al registrarse
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, description="Mínimo 8 caracteres papá")

# 2. Lo que le respondemos al cliente
class UserResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr
    is_active: bool

    model_config = {
        "from_attributes": True
    }

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8, description="Mínimo 8 caracteres si la cambias")