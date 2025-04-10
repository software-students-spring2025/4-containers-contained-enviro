import sys
import os
import pytest
from unittest.mock import MagicMock, patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app as flask_app_module

@pytest.fixture
def test_client():
    """
    Fixture that patches get_database() to prevent a real Mongo connection
    and returns a Flask test client for route testing.
    """
    with patch("app.get_database") as mock_get_db:
        # Return a MagicMock DB object
        mock_get_db.return_value = MagicMock()

        # Enable testing mode on the Flask app
        flask_app_module.config["TESTING"] = True
        
        # Provide Flask's test client to the test
        with flask_app_module.test_client() as client:
            yield client
