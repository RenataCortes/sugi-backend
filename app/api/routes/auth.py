from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.api.deps import get_current_user
from app.core.security import create_access_token

from app.services.auth import register_new_user, authenticate_user
from app.repositories.user import get_user_by_email # Solo para el forgot password temporal

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await register_new_user(db, user_data)

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    return await authenticate_user(db, form_data.username, form_data.password)

@router.post("/refresh")
async def refresh_token(current_user: UserResponse = Depends(get_current_user)):
    new_access_token = create_access_token(data={"sub": current_user.email})
    return {"access_token": new_access_token, "token_type": "bearer"}

@router.post("/forgot-password")
async def forgot_password(email: str, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, email=email)
    # TODO: Lógica de envío de correos en el futuro- aun no se haace
    return {"message": "Si el correo existe en nuestros registros, te enviaremos las instrucciones de recuperación."}