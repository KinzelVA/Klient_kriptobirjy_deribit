from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.services.deribit_client import DeribitClient


@pytest.mark.asyncio
async def test_get_index_price_success():
    client = DeribitClient()

    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json = AsyncMock(return_value={
        "result": {
            "index_price": 70123.45,
        }
    })

    mock_get_context_manager = AsyncMock()
    mock_get_context_manager.__aenter__.return_value = mock_response
    mock_get_context_manager.__aexit__.return_value = None

    mock_session = MagicMock()
    mock_session.get.return_value = mock_get_context_manager

    mock_session_context_manager = AsyncMock()
    mock_session_context_manager.__aenter__.return_value = mock_session
    mock_session_context_manager.__aexit__.return_value = None

    with patch("aiohttp.ClientSession", return_value=mock_session_context_manager):
        price = await client.get_index_price("btc_usd")

    assert price == Decimal("70123.45")


@pytest.mark.asyncio
async def test_get_index_price_invalid_response():
    client = DeribitClient()

    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json = AsyncMock(return_value={"result": {}})

    mock_get_context_manager = AsyncMock()
    mock_get_context_manager.__aenter__.return_value = mock_response
    mock_get_context_manager.__aexit__.return_value = None

    mock_session = MagicMock()
    mock_session.get.return_value = mock_get_context_manager

    mock_session_context_manager = AsyncMock()
    mock_session_context_manager.__aenter__.return_value = mock_session
    mock_session_context_manager.__aexit__.return_value = None

    with patch("aiohttp.ClientSession", return_value=mock_session_context_manager):
        with pytest.raises(ValueError):
            await client.get_index_price("btc_usd")