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
    return render_template("homepage.html")


@app.route("/login")
def login():
    """Login path"""
    return render_template("login.html")


@app.route("/register")
def register():
    """Register path"""
    return render_template("register.html")


@app.route("/movie/<movie_title>")
def movie_page(movie_title):
    """Individual movie path"""
    # movie_obj = movie_collection.find_one({"title": movie_title})
    movie_obj = movie_title  # placeholder
    return render_template("movie_page.html", movie=movie_obj)


@app.route("/movies_saved")
def movies_saved():
    """Movies saved path"""
    return render_template("movies_saved.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("PORT", 5001), debug=True)