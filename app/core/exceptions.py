from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse

# Importamos nuestros errores nativos
from app.core.errors import (InactiveUserError, InvalidCredentialsError,
                             SugiException, UserNotFoundError)


def setup_exception_handlers(app: FastAPI):
    
    # 1. EL TRADUCTOR DE ERRORES DE DOMINIO (El nuevo)
    @app.exception_handler(SugiException)
    async def sugi_custom_exception_handler(request: Request, exc: SugiException):
        # Por defecto asignamos un 400 (Bad Request)
        status_code = status.HTTP_400_BAD_REQUEST
        
        # Mapeamos los errores específicos a su código HTTP correcto
        if isinstance(exc, UserNotFoundError):
            status_code = status.HTTP_404_NOT_FOUND
        elif isinstance(exc, InvalidCredentialsError):
            status_code = status.HTTP_401_UNAUTHORIZED
        elif isinstance(exc, InactiveUserError):
            status_code = status.HTTP_403_FORBIDDEN
            
        return JSONResponse(
            status_code=status_code,
            content={
                "error": True,
                "message": exc.message
            },
        )

     # 2. Los que ya teníamos...
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": True, "message": exc.detail},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Aquí extraemos los mensajes de forma amigable para que sean serializables
        errors = []
        for error in exc.errors():
            errors.append({
                "loc": error["loc"],
                "msg": str(error["msg"]), # Convertimos explícitamente a string
                "type": error["type"]
           })
        
        return JSONResponse(
            status_code=422,
            content={"detail": errors},
       )


    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
        print(f"Error fatal de BD: {exc}") # Para que tú lo veas en la terminal
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": True,
                "message": "Ocurrió un problema interno en la base de datos. Intenta más tarde."
            },
        )