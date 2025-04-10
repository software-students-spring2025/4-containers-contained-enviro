"""Flask web application with MongoDB integration."""

import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(
    __name__, template_folder="templates", static_folder="static", static_url_path="/"
)
app.secret_key = os.getenv("SECRET_KEY", "your-secret-key-here")


def get_database():
    """Get MongoDB database connection."""
    try:
        mongo_user = os.getenv("MONGO_USER", "ml_user")
        mongo_password = os.getenv("MONGO_PASSWORD", "ml_password")
        mongo_host = os.getenv("MONGO_HOST", "mongodb")
        mongo_port = os.getenv("MONGO_PORT", "27017")
        mongo_db = os.getenv("MONGO_DB", "ml_data")

        mongo_url = (
            f"mongodb://{mongo_user}:{mongo_password}@"
            f"{mongo_host}:{mongo_port}/{mongo_db}"
        )

        client = MongoClient(mongo_url, maxPoolSize=50, waitQueueTimeoutMS=2000)
        client.admin.command("ismaster")  # Test connection
        logger.info("Successfully connected to MongoDB")

        return client[mongo_db]

    except ConnectionFailure as e:
        logger.error("Failed to connect to MongoDB: %s", str(e))
        raise
    except OperationFailure as e:
        logger.error("Authentication failed: %s", str(e))
        raise
    except Exception as e:
        logger.error("An error occurred while connecting to MongoDB: %s", str(e))
        raise


# init of database collections
users_collection = None
movies_collection = None
sensor_data_collection = None
ml_results_collection = None


def init_collections():
    global users_collection, movies_collection, sensor_data_collection, ml_results_collection
    if not all([users_collection, movies_collection, sensor_data_collection, ml_results_collection]):
        db = get_database()
        users_collection = db.users
        movies_collection = db.movies
        sensor_data_collection = db.sensor_data
        ml_results_collection = db.ml_results


@app.route("/")
def index():
    init_collections()
    return render_template("homepage.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    init_collections()
    if request.method == "POST":
        try:
            username = request.form.get("username")
            password = request.form.get("password")

            user = users_collection.find_one({"username": username})
            if user and check_password_hash(user["password"], password):
                session["user_id"] = str(user["_id"])
                flash("Login successful!", "success")
                return redirect(url_for("index"))
            flash("Invalid username or password", "error")
        except OperationFailure:
            flash("Database error occurred", "error")
            logger.error("Database error in login route")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    init_collections()
    if request.method == "POST":
        try:
            username = request.form.get("username")
            password = request.form.get("password")

            if users_collection.find_one({"username": username}):
                flash("Username already exists", "error")
            else:
                hashed_password = generate_password_hash(password)
                users_collection.insert_one({
                    "username": username,
                    "password": hashed_password,
                    "saved_movies": [],
                })
                flash("Registration successful!", "success")
                return redirect(url_for("login"))
        except OperationFailure:
            flash("Database error occurred", "error")
            logger.error("Database error in register route")

    return render_template("register.html")


@app.route("/movie/<movie_title>")
def movie_page(movie_title):
    init_collections()
    try:
        movie_obj = movies_collection.find_one({"title": movie_title})
        if not movie_obj:
            flash("Movie not found", "error")
            return redirect(url_for("index"))
        return render_template("movie_page.html", movie=movie_obj)
    except OperationFailure:
        flash("Database error occurred", "error")
        logger.error("Database error in movie_page route")
        return redirect(url_for("index"))


@app.route("/movies_saved")
def movies_saved():
    init_collections()
    try:
        if "user_id" not in session:
            flash("Please log in to view saved movies", "error")
            return redirect(url_for("login"))

        user = users_collection.find_one({"_id": session["user_id"]})
        if user:
            saved_movies = movies_collection.find(
                {"_id": {"$in": user.get("saved_movies", [])}}
            )
            return render_template("movies_saved.html", movies=saved_movies)
        return render_template("movies_saved.html", movies=[])
    except OperationFailure:
        flash("Database error occurred", "error")
        logger.error("Database error in movies_saved route")
        return render_template("movies_saved.html", movies=[])


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("PORT", 5001), debug=True)
