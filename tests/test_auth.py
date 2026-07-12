import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock
import uuid

from app.main import app
from app.core.database import get_db
from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.core.security import hash_password, verify_password


@pytest.fixture
def mock_db():
    session = AsyncMock()
    return session


@pytest.mark.anyio
async def test_password_hashing():
    password = "SuperSecretPassword123"
    hashed = hash_password(password)
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrong_password", hashed) is False


def test_signup_login_flow(monkeypatch):
    # Mock database session injection
    mock_session = AsyncMock()
    app.dependency_overrides[get_db] = lambda: mock_session

    # Mock user repository methods
    mock_user = User(
        id=uuid.uuid4(),
        email="test_user@nadhi.com",
        password_hash=hash_password("MySecurePassword")
    )

    async def mock_get_by_email(self, email):
        if email == "test_user@nadhi.com":
            return mock_user
        return None

    async def mock_create(self, user_obj):
        user_obj.id = uuid.uuid4()
        return user_obj

    monkeypatch.setattr(UserRepository, "get_by_email", mock_get_by_email)
    monkeypatch.setattr(UserRepository, "create", mock_create)

    client = TestClient(app)

    # Test local login with wrong credentials
    resp = client.post("/api/v1/auth/login", json={
        "email": "test_user@nadhi.com",
        "password": "wrong_password"
    })
    assert resp.status_code == 401

    # Test local login with correct credentials
    resp = client.post("/api/v1/auth/login", json={
        "email": "test_user@nadhi.com",
        "password": "MySecurePassword"
    })
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["user_id"] == str(mock_user.id)

    app.dependency_overrides.clear()
