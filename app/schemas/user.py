import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from app.models.user import Role


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str = Field(..., min_length=8, description="Mínimo 8 caracteres")

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