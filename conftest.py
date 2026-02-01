"""Root conftest to set up Python path before test collection."""
import sys
import os

# Add tests directory to path BEFORE any test imports
# Use absolute path to ensure it works in all environments
tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tests'))
if tests_dir not in sys.path:
    sys.path.insert(0, tests_dir)

# Fallback: manually ensure homeassistant is in sys.modules if it's missing
# but exists in our tests directory.
if 'homeassistant' not in sys.modules:
    try:
        import homeassistant
    except ImportError:
        pass
