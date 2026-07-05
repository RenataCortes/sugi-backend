from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth, users
from app.core.config import settings
from app.core.exceptions import setup_exception_handlers

app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0")

# Incluimos los routers
app.include_router(auth.router)
app.include_router(users.router)

# Aquí definimos quién tiene permiso de conectarse a nuestra API desde un frontend
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # Dominios que pueden pasar
    allow_credentials=True,      # Permite enviar el Token JWT en los headers
    allow_methods=["*"],         # Permite todos los métodos (GET, POST, PUT, DELETE)
    allow_headers=["*"],         # Permite todas las cabeceras personalizadas
)
setup_exception_handlers(app)

app.include_router(auth.router)
app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "API Activa. Visita /docs para la documentación interactiva."}

@app.get("/health", tags=["health"])
async def health_check():
    """Endpoint para verificar que el backend este en funcionamiento."""
    return {
        "status": "active",
        "environment": "development", 
        "version": "1.0.0"
    }