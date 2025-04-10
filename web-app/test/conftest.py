"""Pytest configuration and client fixture for testing Flask app."""

import sys
import os
import pytest
from app import app


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

@pytest.fixture
def test_client():
    """Provides a test client for the Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
