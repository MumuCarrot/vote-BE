from unittest.mock import AsyncMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture
def async_session_mock() -> AsyncSession:
    """
    Simple AsyncSession mock for service layer tests.
    """
    return AsyncMock(spec=AsyncSession)


