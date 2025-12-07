"""
Pytest configuration and fixtures for Immunis test suite.
"""

import pytest
import os
import sys

# Add the parent directory to the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture(scope="session")
def threshold_high():
    """Score threshold for definite attacks (should be >= 70)"""
    return 70


@pytest.fixture(scope="session")
def threshold_medium():
    """Score threshold for suspicious prompts (should be >= 40)"""
    return 40


@pytest.fixture(scope="session")
def threshold_low():
    """Score threshold for potentially suspicious (should be >= 20)"""
    return 20


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "expensive: marks tests that make many API calls"
    )


def pytest_collection_modifyitems(config, items):
    """Auto-mark tests based on class name."""
    for item in items:
        if "TestEdgeCases" in item.nodeid:
            item.add_marker(pytest.mark.slow)
        if "TestStatistics" in item.nodeid:
            item.add_marker(pytest.mark.expensive)
