import uuid
import enum
from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, Integer, Float, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base 

class Role(str, enum.Enum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    # Fechas: SQLAlchemy se encarga de la zona horaria UTC
    registration_date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    # onupdate hace que cambie sola cada vez que el usuario haga un cambio en su registro
    last_activity = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    streak_days = Column(Integer, default=0)
    percentage_domain = Column(Float, default=0.0)
    seconds_time_spent = Column(Integer, default=0)
    
    role = Column(String, default="student")
    is_active = Column(Boolean, default=True, index=True)