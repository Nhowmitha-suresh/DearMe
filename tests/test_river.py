import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime, date
import uuid

from app.services.river_service import RiverService
from app.models.health import WaterGoal, WaterLog, SleepLog
from app.models.learning import LearningSession
from app.models.mood import MoodLog
from app.models.journal import JournalEntry
from app.models.tasks import Task
from app.models.placement import Application


@pytest.mark.anyio
async def test_river_state_calculation_defaults():
    # Arrange
    session = AsyncMock()
    
    # Mock database results to return empty/None to test default values
    mock_execute = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = None
    mock_result.scalar.return_value = None
    mock_result.scalar_one.return_value = 0
    mock_execute.return_value = mock_result
    session.execute = mock_execute

    service = RiverService(session)
    user_id = uuid.uuid4()

    # Act
    state = await service.get_river_state(user_id)

    # Assert
    assert "flow_rate" in state
    assert "water_clarity" in state
    assert "flora_density" in state
    assert "wildlife_count" in state
    assert "active_bridges" in state
    assert "current_weather" in state
    assert "time_of_day" in state
    
    # Default outputs when database is empty
    assert state["flow_rate"] == 0.5  # Zero study time
    assert state["water_clarity"] == 0.0  # Zero water intake
    assert state["flora_density"] == 0.25  # Zero mood/journal gives base (5/10)*0.5 = 0.25
    assert state["wildlife_count"] == 6  # Default sleep quality 3 * 2 = 6
    assert state["active_bridges"] == 0  # Zero applications and completed tasks
