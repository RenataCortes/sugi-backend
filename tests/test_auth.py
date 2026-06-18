import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import get_db
from app.models.user import User
from app.core.security import get_password_hash
from datetime import datetime, timezone
from app.api.deps import get_current_user
from app.schemas.user import UserResponse
import uuid

client = TestClient(app)

# 1. Hacemos que nuestra base falsa pueda recibir un "usuario prefabricado"
class MockAsyncSession:
    def __init__(self, fake_user_to_return=None):
        self.fake_user_to_return = fake_user_to_return

    async def execute(self, *args, **kwargs):
        class MockResult:
            def scalars(self_inner):
                class MockScalars:
                    def first(self_inner2):
                        # Devuelve el usuario prefabricado, o None si no hay
                        return self.fake_user_to_return
                return MockScalars()
        return MockResult()

    def add(self, *args, **kwargs):
        pass

    async def commit(self):
        pass

    async def refresh(self, obj):
        obj.id = uuid.uuid4()
        obj.registration_date = datetime.now(timezone.utc)
        obj.last_activity = datetime.now(timezone.utc)
        obj.streak_days = 0
        obj.percentage_domain = 0.0
        obj.seconds_time_spent = 0
        obj.is_active = True

# --- INICIAN LOS TESTS ---

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
    assert response.json()["email"] == payload["email"]

def test_login_success():
    fake_user = User(
        id=uuid.uuid4(),
        email="yoel.test@example.com",
        hashed_password=get_password_hash("Password123!"),
        is_active=True
    )
    
    app.dependency_overrides[get_db] = lambda: MockAsyncSession(fake_user_to_return=fake_user)
    
    login_data = {
        "username": "yoel.test@example.com",
        "password": "Password123!"
    }
    
    response = client.post("/auth/login", data=login_data)
    
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_wrong_password():
    fake_user = User(
        id=uuid.uuid4(),
        email="yoel.test@example.com",
        hashed_password=get_password_hash("Password123!"),
        is_active=True
    )
    
    app.dependency_overrides[get_db] = lambda: MockAsyncSession(fake_user_to_return=fake_user)
    
    login_data = {
        "username": "yoel.test@example.com",
        "password": "Dianita2428"
    }
    
    response = client.post("/auth/login", data=login_data)
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Correo o contraseña incorrectos, papu"
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
        is_active=True
    )
    
    app.dependency_overrides[get_current_user] = lambda: fake_current_user
    
    response = client.post("/auth/refresh")
    
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
    
    app.dependency_overrides.pop(get_current_user, None)

def test_forgot_password():
    """
    Prueba que el endpoint de recuperación siempre devuelva el mismo mensaje
    por seguridad, sin importar si el correo existe o no.
    """

    app.dependency_overrides[get_db] = lambda: MockAsyncSession(fake_user_to_return=None)
    
    response = client.post("/auth/forgot-password?email=hacker@ejemplo.com")
    
    assert response.status_code == 200
    assert "instrucciones de recuperación" in response.json()["message"]
    