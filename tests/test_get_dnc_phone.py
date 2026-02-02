from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import get_session
from app.main import app


@pytest.fixture()
def override_db_session():
    def _override(mock_result):
        mock_session = AsyncMock(spec=AsyncSession)
        mock_session.execute = AsyncMock(return_value=mock_result)

        async def override_get_session():
            yield mock_session

        app.dependency_overrides[get_session] = override_get_session
        return mock_session

    try:
        yield _override
    finally:
        app.dependency_overrides.clear()


def test_get_phone_when_found_with_reason(override_db_session):
    """Test that get_phone endpoint returns the reason when a DNC phone is found."""
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = SimpleNamespace(reason="customer_request")

    override_db_session(mock_result)

    client = TestClient(app)
    response = client.get("/dnc_phone/org-1/campaign-1/+15551234567")

    assert response.status_code == 200
    assert response.json() == "customer_request"


def test_get_phone_when_found_with_empty_reason(override_db_session):
    """Test that get_phone endpoint returns the reason when a DNC phone is found."""
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = SimpleNamespace(reason="")

    override_db_session(mock_result)

    client = TestClient(app)
    response = client.get("/dnc_phone/org-1/campaign-1/+15551234567")

    assert response.status_code == 200
    assert response.json() == ""


def test_get_phone_when_not_found(override_db_session):
    """Test that get_phone endpoint returns None when a DNC phone is not found."""
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None

    override_db_session(mock_result)

    client = TestClient(app)
    response = client.get("/dnc_phone/org-1/campaign-1/+15559999999")

    assert response.status_code == 200
    assert response.json() is None
