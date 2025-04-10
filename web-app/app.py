"""Flask app"""
# pylint: disable=unused-import, method-hidden
# pylint: enable=too-many-lines
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from flask_bcrypt import Bcrypt
from bson.objectid import ObjectId
from dotenv import load_dotenv

load_dotenv()

app = Flask(
    __name__, template_folder="templates", static_folder="static", static_url_path="/"
)
app.secret_key = os.getenv("SECRET_KEY")

bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)
login_manager.login_message = ""


class User(UserMixin):
    """For flask login"""

    def __init__(self, user_data):
        self.id = str(user_data["_id"])
        self.username = user_data["username"]
        self.password_hash = user_data["password"]

    def get_id(self):
        return self.id

    @staticmethod
    def validate_login(password_hash, password):
        """Validate login"""
        return bcrypt.check_password_hash(password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    """Loads user"""
    user_data = users_collection.find_one({"_id": ObjectId(user_id)})
    if not user_data:
        return None
    return User(user_data)


@app.route("/")
def index():
    """Default path"""
    return render_template("homepage.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login path"""
    if current_user.is_authenticated:
        return redirect(url_for("/"))

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_data = users_collection.find_one({"username": username})

        if user_data:
            if bcrypt.check_password_hash(user_data["password"], password):
                user = User(user_data)
                login_user(user)

                next_page = request.args.get("next")
                return redirect(next_page if next_page else url_for("/"))
            flash("Invalid password. Please try again.", "danger")
        else:
            flash("User does not exist. Please try again.", "danger")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register path"""
    if current_user.is_authenticated:
        return redirect(url_for("/"))

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        existing_user = users_collection.find_one({"username": username})

        if existing_user is None:
            hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

            users_collection.insert_one(
                {"username": username, "password": hashed_password}
            )
            return redirect(url_for("login"))
        flash("Username already exists. Please choose a different one.", "danger")

    return render_template("register.html")


@app.route("/movie/<movie_title>")
@login_required
def movie_page(movie_title):
    """Individual movie path"""
    # movie_obj = movie_collection.find_one({"title": movie_title})
    movie_obj = movie_title  # placeholder
    return render_template("movie_page.html", movie=movie_obj)


@app.route("/movies_saved")
@login_required
def movies_saved():
    """Movies saved path"""
    return render_template("movies_saved.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("PORT", 5001), debug=True)
