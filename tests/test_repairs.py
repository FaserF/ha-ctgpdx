"""Tests for the CTGP-DX repair issues."""

import sys
import os
from datetime import datetime, timezone, timedelta

# Fail-safe path injection
tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tests"))
if tests_dir not in sys.path:
    sys.path.insert(0, tests_dir)

import pytest  # noqa: E402
from unittest.mock import patch, MagicMock  # noqa: E402
from custom_components.ctgpdx.coordinator import CtgpdxUpdateCoordinator  # noqa: E402


@pytest.mark.asyncio
async def test_repair_issue_creation(mock_hass):
    """Test that a repair issue is created after 24 hours of failure."""
    coordinator = CtgpdxUpdateCoordinator(mock_hass)

    # Set last success to 25 hours ago
    coordinator._last_success_time = datetime.now(timezone.utc) - timedelta(hours=25)

    with (
        patch(
            "custom_components.ctgpdx.coordinator.async_get_clientsession"
        ) as mock_session_factory,
        patch(
            "custom_components.ctgpdx.coordinator.async_create_issue"
        ) as mock_create_issue,
    ):
        mock_session = MagicMock()
        mock_session_factory.return_value = mock_session
        mock_session.get.side_effect = Exception("Connection error")

        with pytest.raises(Exception):
            await coordinator._async_update_data()

        mock_create_issue.assert_called_once()
        assert mock_create_issue.call_args[0][2] == "website_change"


@pytest.mark.asyncio
async def test_repair_issue_deletion(mock_hass):
    """Test that a repair issue is deleted after a successful update."""
    coordinator = CtgpdxUpdateCoordinator(mock_hass)

    with (
        patch(
            "custom_components.ctgpdx.coordinator.async_get_clientsession"
        ) as mock_session_factory,
        patch(
            "custom_components.ctgpdx.coordinator.async_delete_issue"
        ) as mock_delete_issue,
    ):
        mock_session = MagicMock()
        mock_session_factory.return_value = mock_session
        mock_response = MagicMock()

        async def mock_text():
            return "Version: 1.1.1"

        mock_response.text = mock_text
        mock_response.raise_for_status = MagicMock()

        class MockContextManager:
            async def __aenter__(self):
                return mock_response

            async def __aexit__(self, *args):
                pass

        mock_session.get.return_value = MockContextManager()

        await coordinator._async_update_data()

        mock_delete_issue.assert_called_once_with(mock_hass, "ctgpdx", "website_change")
