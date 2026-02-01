"""Mock frame helper for tests."""


class _HassContext:
    """Container for hass context variable."""

    def __init__(self):
        self.hass = None


_hass = _HassContext()


def report_usage(*args, **kwargs):
    """Mock report_usage that does nothing - completely bypasses all frame checking."""
    return None
