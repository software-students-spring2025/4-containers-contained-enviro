"""Flask app exposing a simple test route."""

from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    """Return a simple test message to confirm the app is working."""
    return "Flask works"
