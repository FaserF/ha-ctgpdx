"""Tests for the CTGP-DX scraping robustness."""

import sys
import os

# Fail-safe path injection
tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tests"))
if tests_dir not in sys.path:
    sys.path.insert(0, tests_dir)

import pytest  # noqa: E402
from unittest.mock import patch, MagicMock  # noqa: E402
from custom_components.ctgpdx.coordinator import CtgpdxUpdateCoordinator  # noqa: E402


@pytest.mark.asyncio
async def test_robustness_varied_html(mock_hass):
    """Test scraping with varied HTML structures and casing."""
    coordinator = CtgpdxUpdateCoordinator(mock_hass)

    varied_html = """
    <html>
        <body>
            <div>
                <span>VERSION: 1.2.3b</span>
                <p>DOWNLOAD   SIZE: 1.5 GB</p>
                <p>UNPACKED SIZE: 2.0 gb</p>
            </div>
            <section>
                <h2>Changelog</h2>
                <p>v1.2.3b - April 10th, 2025: Some changes</p>
            </section>
        </body>
    </html>
    """

    with patch(
        "custom_components.ctgpdx.coordinator.async_get_clientsession"
    ) as mock_session_factory:
        mock_session = MagicMock()
        mock_session_factory.return_value = mock_session
        mock_response = MagicMock()

        async def mock_text():
            return varied_html

        mock_response.text = mock_text
        mock_response.raise_for_status = MagicMock()

        class MockContextManager:
            async def __aenter__(self):
                return mock_response

            async def __aexit__(self, *args):
                pass

        mock_session.get.return_value = MockContextManager()

        data = await coordinator._async_update_data()

        assert data["version"] == "1.2.3b"
        assert data["download_size"] == "1.5 GB"
        assert data["unpacked_size"] == "2.0 gb"
        assert data["release_date"] == "April 10th, 2025"


@pytest.mark.asyncio
async def test_robustness_fallback_date(mock_hass):
    """Test fallback date extraction when version-specific date is not found."""
    coordinator = CtgpdxUpdateCoordinator(mock_hass)

    html = """
    <html>
        <body>
            <p>Version: 2.0</p>
            <p>Update released on January 1st, 2026</p>
        </body>
    </html>
    """

    with patch(
        "custom_components.ctgpdx.coordinator.async_get_clientsession"
    ) as mock_session_factory:
        mock_session = MagicMock()
        mock_session_factory.return_value = mock_session
        mock_response = MagicMock()

        async def mock_text():
            return html

        mock_response.text = mock_text
        mock_response.raise_for_status = MagicMock()

        class MockContextManager:
            async def __aenter__(self):
                return mock_response

            async def __aexit__(self, *args):
                pass

        mock_session.get.return_value = MockContextManager()

        data = await coordinator._async_update_data()

        assert data["version"] == "2.0"
        assert data["release_date"] == "January 1st, 2026"


@pytest.mark.asyncio
async def test_robustness_messy_whitespace(mock_hass):
    """Test scraping with extremely messy whitespace and newlines."""
    coordinator = CtgpdxUpdateCoordinator(mock_hass)

    html = """
    <html>
        <body>
            Version:

            3.4.5

            Download
            size:
            100
            MB
        </body>
    </html>
    """

    with patch(
        "custom_components.ctgpdx.coordinator.async_get_clientsession"
    ) as mock_session_factory:
        mock_session = MagicMock()
        mock_session_factory.return_value = mock_session
        mock_response = MagicMock()

        async def mock_text():
            return html

        mock_response.text = mock_text
        mock_response.raise_for_status = MagicMock()

        class MockContextManager:
            async def __aenter__(self):
                return mock_response

            async def __aexit__(self, *args):
                pass

        mock_session.get.return_value = MockContextManager()

        data = await coordinator._async_update_data()

        assert data["version"] == "3.4.5"
        assert data["download_size"] == "100 MB"


@pytest.mark.asyncio
async def test_robustness_live_site_messy_data(mock_hass):
    """Test scraping with the specific messy format found on the live site."""
    coordinator = CtgpdxUpdateCoordinator(mock_hass)

    # Note the spaces in "1. 1.1" and "size :" and "s ize"
    html = """
    <html>
        <body>
            <p>Version: 1. 1.1</p>
            <p>Download size : 3.86 GB</p>
            <p>Unpacked s ize: 4.52 GB</p>
        </body>
    </html>
    """

    with patch(
        "custom_components.ctgpdx.coordinator.async_get_clientsession"
    ) as mock_session_factory:
        mock_session = MagicMock()
        mock_session_factory.return_value = mock_session
        mock_response = MagicMock()

        async def mock_text():
            return html

        mock_response.text = mock_text
        mock_response.raise_for_status = MagicMock()

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
