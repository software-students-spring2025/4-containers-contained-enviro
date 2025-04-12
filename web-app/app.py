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
app.secret_key = os.getenv("SECRET_KEY", "movie-secret-key")

if not os.getenv("FLASK_TESTING"):
    from pymongo import MongoClient

    client = MongoClient("mongodb://localhost:27017/")
    db = client["ml_data"]


def get_database():
    """Get MongoDB database connection."""
    try:
        # Get MongoDB connection details from environment variables
        mongo_user = os.getenv("MONGO_USER", "ml_user")
        mongo_password = os.getenv("MONGO_PASSWORD", "ml_password")
        mongo_host = os.getenv("MONGO_HOST", "mongodb")
        mongo_port = os.getenv("MONGO_PORT", "27017")
        mongo_db = os.getenv("MONGO_DB", "ml_data")

        # Create MongoDB connection URL
        mongo_url = (
            f"mongodb://{mongo_user}:{mongo_password}@"
            f"{mongo_host}:{mongo_port}/{mongo_db}"
        )

        # Connect to MongoDB with connection pooling
        client = MongoClient(mongo_url, maxPoolSize=50, waitQueueTimeoutMS=2000)

        # Test connection
        client.admin.command("ismaster")
        logger.info("Successfully connected to MongoDB")

        # Get database
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


# Initialize database collections
try:
    database = get_database()
    users_collection = database.users
    movies_collection = database.movies
    sensor_data_collection = database.sensor_data
    ml_results_collection = database.ml_results
except (ConnectionFailure, OperationFailure) as e:
    logger.error("Failed to connect to MongoDB: %s", str(e))
    raise


# Home page route
@app.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("homepage.html")


# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
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


# Register route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            username = request.form.get("username")
            password = request.form.get("password")

            if users_collection.find_one({"username": username}):
                flash("Username already exists", "error")
            else:
                hashed_password = generate_password_hash(password)
                users_collection.insert_one(
                    {
                        "username": username,
                        "password": hashed_password,
                        "saved_movies": [],
                    }
                )
                flash("Registration successful!", "success")
                return redirect(url_for("login"))
        except OperationFailure:
            flash("Database error occurred", "error")
            logger.error("Database error in register route")

    return render_template("register.html")


# Movie details page route
@app.route("/movie/<movie_title>")
def movie_page(movie_title):
    try:
        if "user_id" not in session:
            flash("Please log in to view movie details", "error")
            return redirect(url_for("login"))
        # TODO: fetch by ID
        movie_obj = movies_collection.find_one({"title": movie_title})
        if not movie_obj:
            flash("Movie not found", "error")
            return redirect(url_for("index"))
        return render_template("movie_page.html", movie=movie_obj)
    except OperationFailure:
        flash("Database error occurred", "error")
        logger.error("Database error in movie_page route")
        return redirect(url_for("index"))

#  Saved movies page route.
@app.route("/movies_saved")
def movies_saved():
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


# Logout route
@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out", "success")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("PORT", 5001), debug=True)
