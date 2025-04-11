"""Pytest configuration and test client fixture for the Flask web app."""

import pytest
from app import app as flask_app


@pytest.fixture
def client():
    """Provides a test client for the Flask app."""
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client
