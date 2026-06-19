import math

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate
from app.schemas.pagination import PaginatedResponse
from app.api.deps import get_current_user, get_pagination_params

from app.repositories.user import (
    update_user, 
    delete_user, 
    get_all_users_paginated, 
    get_users_count
)

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=PaginatedResponse[UserResponse])
async def read_all_users(
    pagination: dict = Depends(get_pagination_params),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtiene la lista de todos los usuarios con metadatos de paginación."""
    
    skip = pagination["skip"]
    limit = pagination["limit"]
    
    # 1. Traemos los datos y el total desde Postgres
    users = await get_all_users_paginated(db=db, skip=skip, limit=limit)
    total_users = await get_users_count(db)
    
    # 2. Hacemos la matemática de los metadatos
    current_page = (skip // limit) + 1
    total_pages = math.ceil(total_users / limit) if total_users > 0 else 1
    
    # 3. Armamos la respuesta perfecta
    return {
        "data": users,
        "meta": {
            "total_records": total_users,
            "current_page": current_page,
            "total_pages": total_pages,
            "has_next": current_page < total_pages,
            "has_previous": current_page > 1
        }
    }

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Obtiene el perfil del usuario autenticado."""
    return current_user

@router.put("/me", response_model=UserResponse)
async def update_user_me(
    user_in: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Actualiza el perfil del usuario autenticado."""
    updated_user = await update_user(db, db_user=current_user, user_in=user_in)
    return updated_user

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_me(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Borra la cuenta del usuario autenticado. 
    Devuelve un 204 (Sin contenido) si fue exitoso.
    """
    await delete_user(db, db_user=current_user)
    return None