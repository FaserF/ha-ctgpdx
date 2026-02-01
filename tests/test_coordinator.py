"""Tests for the CTGP-DX coordinator scraping logic."""

import sys
import os

# Fail-safe path injection to ensure homeassistant mock is found during collection
tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tests"))
if tests_dir not in sys.path:
    sys.path.insert(0, tests_dir)

import pytest  # noqa: E402
from unittest.mock import patch, MagicMock  # noqa: E402
from custom_components.ctgpdx.coordinator import CtgpdxUpdateCoordinator  # noqa: E402
from homeassistant.helpers.update_coordinator import UpdateFailed  # noqa: E402


@pytest.mark.asyncio
async def test_coordinator_scraping(mock_hass, sample_html):
    """Test the scraping logic in the coordinator."""
    coordinator = CtgpdxUpdateCoordinator(mock_hass)

    # Mock the web request
    with patch(
        "custom_components.ctgpdx.coordinator.async_get_clientsession"
    ) as mock_session_factory:
        mock_session = MagicMock()
        mock_session_factory.return_value = mock_session

        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()

        # Async mock for text()
        async def mock_text():
            return sample_html

        mock_response.text = mock_text

        # Async context manager for session.get()
        class MockContextManager:
            async def __aenter__(self):
                return mock_response

            async def __aexit__(self, *args):
                pass

        mock_session.get.return_value = MockContextManager()

        data = await coordinator._async_update_data()

        assert data["version"] == "1.1.1"
        assert data["download_size"] == "3.86 GB"
        assert data["unpacked_size"] == "4.52 GB"
        assert data["release_date"] == "March 23rd, 2025"


@pytest.mark.asyncio
async def test_coordinator_scraping_error(mock_hass):
    """Test handling of connection errors."""
    coordinator = CtgpdxUpdateCoordinator(mock_hass)

    with patch(
        "custom_components.ctgpdx.coordinator.async_get_clientsession"
    ) as mock_session_factory:
        mock_session = MagicMock()
        mock_session_factory.return_value = mock_session

        # Mock a ClientError
        from aiohttp import ClientError

        mock_session.get.side_effect = ClientError("Connection failed")

        with pytest.raises(UpdateFailed):
            await coordinator._async_update_data()
