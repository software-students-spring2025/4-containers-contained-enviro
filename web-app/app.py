"""Flask app"""
# pylint: disable=unused-import, method-hidden
# pylint: enable=too-many-lines
import os
from flask import Flask, render_template, request, redirect, url_for, flash

# from flask_login import (
#     LoginManager,
#     UserMixin,
#     login_user,
#     logout_user,
#     login_required,
#     current_user,
# )

app = Flask(
    __name__, template_folder="templates", static_folder="static", static_url_path="/"
)
app.secret_key = os.getenv("SECRET_KEY")


@app.route("/")
def index():
    """Default path"""
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("PORT", 5001), debug=True)

print("Delete this")
