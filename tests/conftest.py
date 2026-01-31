"""Fixtures for CTGP-DX tests."""
import pytest
from unittest.mock import MagicMock

@pytest.fixture
def mock_hass():
    """Mock Home Assistant."""
    hass = MagicMock()
    # Add any necessary hass methods here
    return hass

@pytest.fixture
def sample_html():
    """Return sample HTML from the CTGP-DX download page."""
    return """
    <html>
        <body>
            <h1>Download</h1>
            <p>Important: The latest version of CTGP Deluxe (1.1.1) only works on Mario Kart 8 Deluxe version 3.0.3</p>
            <p>Version: 1.1.1</p>
            <p>Download size: 3.86 GB</p>
            <p>Unpacked size: 4.52 GB</p>
            <h2>Changelogs</h2>
            <h3>v1.1.1 - March 23rd, 2025</h3>
        </body>
    </html>
    """
