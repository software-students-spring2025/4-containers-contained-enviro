"""Pytest configuration and test client fixture for the Flask web app."""

import pytest
from app import app as flask_app

@pytest.fixture
def client():
    """Fixture to return a Flask test client for use in test cases."""
    return flask_app.test_client()
