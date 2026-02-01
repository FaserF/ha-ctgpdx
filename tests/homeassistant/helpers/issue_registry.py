"""Mock for homeassistant.helpers.issue_registry."""
from enum import StrEnum

class IssueSeverity(StrEnum):
    """Issue severity."""
    CRITICAL = "critical"
    ERROR = "error"
    WARNING = "warning"

async def async_create_issue(hass, domain, issue_id, **kwargs):
    """Create an issue."""
    pass

async def async_delete_issue(hass, domain, issue_id):
    """Delete an issue."""
    pass
