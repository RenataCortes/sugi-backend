import uuid
from datetime import datetime, timezone
from fastapi.testclient import TestClient

from app.main import app
from app.schemas.user import UserResponse
from app.models.user import User
from app.core.security import get_password_hash
from app.core.database import get_db

class DummyScalars:
    def __init__(self, data):
        self.data = data
        
    def first(self):
        return self.data
        
    def all(self):
        return [self.data] if self.data else []

class MockResult:
    def __init__(self, fake_data):
        self.fake_data = fake_data
        
    def scalar_one_or_none(self):
        return self.fake_data
        
    def scalars(self):
        # Ahora pasamos el dato explícitamente a la clase externa
        return DummyScalars(self.fake_data)

class MockAsyncSession:
    def __init__(self, fake_user_to_return=None):
        self.fake_user_to_return = fake_user_to_return

    async def execute(self, query, *args, **kwargs):
        return MockResult(self.fake_user_to_return)

    def add(self, instance):
        pass 

    async def commit(self):
        pass 

    async def refresh(self, instance):
        pass
# ==========================================

client = TestClient(app)

# 1. TEST DE VALIDACIÓN (El nuevo Nivel Dios)
def test_validation_error_handler():
    """
    Prueba que si enviamos un correo falso o nos faltan datos, 
    FastAPI atrape el error 422 y nos devuelva nuestro JSON estandarizado.
    """
    response = client.post(
        "/auth/register",
        json={
            "first_name": "Papu",
            # Falta last_name, password, y el correo está chueco
            "email": "esto-no-es-un-correo" 
        }
    )
    
    assert response.status_code == 422
    data = response.json()
    assert data["error"] is True
    assert "Los datos enviados no son válidos" in data["message"]
    assert "details" in data 

# 2. TEST DE REGISTRO EXITOSO
def test_register_user_success():
    app.dependency_overrides[get_db] = lambda: MockAsyncSession(fake_user_to_return=None)
    
    payload = {
        "first_name": "Yoel",
        "last_name": "Canul",
        "email": "yoel.test@example.com",
        "password": "Password123!"
    }
    
    response = client.post("/auth/register", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == payload["email"]
    assert "role" in data # Pydantic validará que traiga el rol 'student' por defecto

# 3. TEST DE LOGIN EXITOSO (El que ya tenías en verde)
def test_login_success():
    fake_user = User(
        id=uuid.uuid4(),
        email="yoel.test@example.com",
        hashed_password=get_password_hash("Password123!"),
        is_active=True,
        role="student"
    )
    
    app.dependency_overrides[get_db] = lambda: MockAsyncSession(fake_user_to_return=fake_user)
    
    login_data = {
        "username": "yoel.test@example.com",
        "password": "Password123!"
    }
    
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()

# 4. TEST DE CONTRASEÑA INCORRECTA (Arreglado el key 'message')
def test_login_wrong_password():
    fake_user = User(
        id=uuid.uuid4(),
        email="yoel.test@example.com",
        hashed_password=get_password_hash("Password123!"),
        is_active=True,
        role="student"
    )
    
    app.dependency_overrides[get_db] = lambda: MockAsyncSession(fake_user_to_return=fake_user)
    
    login_data = {
        "username": "yoel.test@example.com",
        "password": "Dianita2428" # Contraseña mala
    }
    
    response = client.post("/auth/login", data=login_data)
    
    assert response.status_code == 401
    # ¡Aquí está la magia de nuestro manejador de errores personalizado!
    assert response.json()["message"] == "Correo o contraseña incorrectos. Revisa tus datos."

# 5. TEST DE REFRESH TOKEN (Arreglado el campo 'role' que pedía Pydantic)
def test_refresh_token_success():
    """
    Prueba que un usuario logueado pueda pedir un token nuevo.
    """
    fake_current_user = UserResponse(
        id=uuid.uuid4(),
        first_name="Yoel",
        last_name="Canul",
        email="yoel.test@example.com",
        registration_date=datetime.now(timezone.utc),
        last_activity=datetime.now(timezone.utc),
        streak_days=0,
        percentage_domain=0.0,
        seconds_time_spent=0,
        is_active=True,
        role="student"  # <--- Esto es lo que hacía que explotara el test
    )
    
    # Aquí asumo que sobreescribes 'get_current_user' en tu test
    from app.api.deps import get_current_user
    app.dependency_overrides[get_current_user] = lambda: fake_current_user
    
    response = client.post("/auth/refresh")
    
    assert response.status_code == 200
    assert "access_token" in response.json()

# 6. TEST DE FORGOT PASSWORD (El que tenías en verde)
def test_forgot_password():
    app.dependency_overrides[get_db] = lambda: MockAsyncSession(fake_user_to_return=True)
    
    response = client.post("/auth/forgot-password?email=yoel.test@example.com")
    assert response.status_code == 200
    assert "message" in response.json()