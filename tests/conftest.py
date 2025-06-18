"""Shared test configuration and fixtures."""

import os
import pytest
from tofupilot import TofuPilotClient


@pytest.fixture
def api_key():
    """Default API key for testing."""
    return os.getenv("TOFUPILOT_API_KEY", "76978854-ee7e-45ac-ba51-394103fdcc4a")


@pytest.fixture
def base_url():
    """Default base URL for testing."""
    return os.getenv("TOFUPILOT_BASE_URL", "http://localhost:3000")


@pytest.fixture
def client(api_key, base_url):
    """Authenticated TofuPilot client instance."""
    return TofuPilotClient(api_key=api_key, base_url=base_url)


@pytest.fixture
def test_serial_number():
    """Test serial number for demo data."""
    return "DEMO-001"


@pytest.fixture
def test_run_id():
    """Test run ID for demo data."""
    return "test-run-123"