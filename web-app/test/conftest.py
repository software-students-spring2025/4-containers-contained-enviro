"""Pytest configuration and client fixture for testing Flask app."""

import sys
import os
import pytest

# Add the web-app/ folder to the path so we can import app.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app  # Keep this after sys.path.insert() for correct import

@pytest.fixture
def test_client():
    """Provides a test client for the Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
