import uuid
from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

# Esta es la clase base de la cual heredarán todos nuestros modelos
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    # UUID nativo de Postgres: indescifrable y súper seguro para los IDs
    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4, 
        unique=True, 
        nullable=False,
        index=True
    )
    
    # Email único e indexado para búsquedas ultra rápidas en el login
    email = Column(String(255), unique=True, index=True, nullable=False)
    
    # Almacenará el hash de bcrypt, nunca el texto plano
    hashed_password = Column(String(255), nullable=False)
    
    # Controles de estado de la cuenta
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)