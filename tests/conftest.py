from unittest.mock import MagicMock

import pytest


@pytest.fixture
def mock_hass():
    """Mock Home Assistant with proper event loop and frame helper setup."""
    import asyncio

    # Import frame here, after sys.path has been set up
    from homeassistant.helpers import frame

    hass = MagicMock()
    # Provide a real event loop for frame.report_usage() which calls run_callback_threadsafe
    # Create a new event loop for the test
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    hass.loop = loop

    # Set the frame helper's _hass ContextVar to our mock
    # This is required because DataUpdateCoordinator checks for the hass context
    original_hass = getattr(frame._hass, "hass", None)
    frame._hass.hass = hass
    yield hass
    # Restore the original value and clean up the event loop
    frame._hass.hass = original_hass
    # Close the event loop to prevent hanging
    loop.close()
    asyncio.set_event_loop(None)


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
