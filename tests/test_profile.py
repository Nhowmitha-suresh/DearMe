import pytest
import uuid
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock

from app.main import app
from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User, UserProfile, UserSetting

def test_profile_endpoints(monkeypatch):
    mock_session = AsyncMock()
    mock_user = User(id=uuid.uuid4(), email="student@nadhi.edu")

    # Override dependencies
    app.dependency_overrides[get_db] = lambda: mock_session
    app.dependency_overrides[get_current_user] = lambda: mock_user

    # Mock execute results
    mock_result_profile = MagicMock()
    mock_result_profile.scalars.return_value.first.return_value = None
    
    mock_result_setting = MagicMock()
    mock_result_setting.scalars.return_value.first.return_value = None
    
    async def mock_execute(q):
        # Determine based on query string representation
        q_str = str(q).lower()
        if "user_profile" in q_str:
            return mock_result_profile
        else:
            return mock_result_setting

    mock_session.execute = mock_execute

    client = TestClient(app)

    # Test POST /api/v1/users/profile
    payload = {
        "first_name": "Aman",
        "last_name": "Sharma",
        "college": "IIT Madras",
        "department": "Computer Science",
        "year": 3,
        "student_roll_no": "CS23B001",
        "gpa": 9.1,
        "skills": ["Flutter", "Python"],
        "target_roles": ["SDE"]
    }
    resp = client.post("/api/v1/users/profile", json=payload)
    assert resp.status_code == 200
    assert resp.json() == {"message": "Profile and placement customizations saved successfully"}

    # Test GET /api/v1/users/profile/me
    mock_profile = UserProfile(
        first_name="Aman",
        last_name="Sharma",
        college="IIT Madras",
        department="Computer Science",
        year=3,
        student_roll_no="CS23B001"
    )
    mock_setting = UserSetting(
        key="placement_profile",
        value={"gpa": 9.1, "skills": ["Flutter", "Python"], "target_roles": ["SDE"]}
    )

    mock_result_profile.scalars.return_value.first.return_value = mock_profile
    mock_result_setting.scalars.return_value.first.return_value = mock_setting

    resp = client.get("/api/v1/users/profile/me")
    assert resp.status_code == 200
    data = resp.json()
    assert data["first_name"] == "Aman"
    assert data["college"] == "IIT Madras"
    assert data["gpa"] == 9.1
    assert "Flutter" in data["skills"]

    app.dependency_overrides.clear()
