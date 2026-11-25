"""Tests for CTGP-DX initialization."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.config_entries import ConfigEntry

from custom_components.ctgpdx import async_setup_entry


@pytest.mark.asyncio
async def test_async_setup_entry(mock_hass):
    """Test that async_setup_entry completes without errors."""
    entry = MagicMock(spec=ConfigEntry)
    entry.entry_id = "test_entry"

    # Mock the coordinator and its methods
    mock_hass.config_entries.async_forward_entry_setups = AsyncMock()

    with patch(
        "custom_components.ctgpdx.CtgpdxUpdateCoordinator"
    ) as mock_coordinator_class:
        mock_coordinator = mock_coordinator_class.return_value
        mock_coordinator.async_config_entry_first_refresh = AsyncMock()

        # Call the setup function
        result = await async_setup_entry(mock_hass, entry)

        assert result is True
        # Verify that async_update_entry was NOT called (which was causing the crash)
        # Note: If it were called, it would likely fail in this mock environment too
        # but we specifically want to ensure the logic that was there is gone.
        mock_hass.config_entries.async_update_entry.assert_not_called()

        # Verify platforms are forwarded
        mock_hass.config_entries.async_forward_entry_setups.assert_called_once()
