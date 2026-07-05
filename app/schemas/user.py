import re
import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.models.user import Role


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str = Field(..., min_length=8)

    @field_validator('password')
    @classmethod
    def password_complexity(cls, v: str) -> str:
        if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}$", v):
            raise ValueError('La contraseña debe tener al menos 8 caracteres, una letra y un número')
        return v

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)

class UserResponse(BaseModel):
    id: uuid.UUID
    first_name: str
    last_name: str
    email: EmailStr
    registration_date: Optional[datetime] = None
    last_activity: Optional[datetime] = None
    streak_days: int
    percentage_domain: float
    seconds_time_spent: int
    is_active: bool
    role: Role

    model_config = {
        "from_attributes": True
    }