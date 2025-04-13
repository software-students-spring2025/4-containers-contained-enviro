"""Flask web application with MongoDB integration."""

import os
import logging
from datetime import datetime
import base64
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    jsonify,
)
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId  # Needed to convert string IDs
import requests

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


# pylint: disable=broad-except
def get_database():
    """Get MongoDB database connection."""
    try:
        # Get MongoDB connection details from environment variables
        mongo_user = os.getenv("MONGO_USER", "ml_user")
        mongo_password = os.getenv("MONGO_PASSWORD", "ml_password")
        mongo_host = os.getenv("MONGO_HOST", "localhost")
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
        # client.admin.command("ismaster")
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


# New endpoint in your web app (added below your existing routes)
@app.route("/upload_recording", methods=["POST"])
def upload_recording():
    """Handle upload_recording route"""
    if "user_id" not in session:
        flash("Please log in to upload recordings", "error")
        return redirect(url_for("login"))
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400
    audio_file = request.files["audio"]
    audio_data = audio_file.read()

    raw_data = {"audio": base64.b64encode(audio_data).decode("utf-8")}

    result = sensor_data_collection.insert_one(
        {
            "user_id": session["user_id"],
            "status": "pending",
            "timestamp": datetime.now(),
            "sensor_type": "microphone",
            "raw_data": raw_data,
        }
    )
    recording_id = str(result.inserted_id)
    try:
        requests.post("http://ml_client:5002/process_pending", timeout=20)
    except Exception as e:
        logger.error("Failed to trigger ML processing: %s", str(e))

    return jsonify({"recording_id": recording_id}), 200


@app.route("/movie/<recording_id>")
def movie_page(recording_id):  # pylint: disable=broad-except
    """Handle individual movie route"""
    if "user_id" not in session:
        flash("Please log in to view movie details", "error")
        return redirect(url_for("login"))
    try:
        prediction = ml_results_collection.find_one(
            {"sensor_data_id": ObjectId(recording_id)}
        )
        if not prediction:
            flash("Movie prediction not found", "error")
            return redirect(url_for("index"))
        movie = movies_collection.find_one(
            {"title": prediction["results"]["predicted_movie"]}
        )
        transcription = prediction["results"]["transcription"]
        return render_template(
            "movie_page.html", movie=movie, transcription=transcription
        )
    except OperationFailure:
        flash("Database error occurred", "error")
        logger.error("Database error in movie_prediction route")
        return redirect(url_for("index"))
    except Exception as e:
        flash("An error occurred", "error")
        logger.error("Error in movie_page route: %s", str(e))
        return redirect(url_for("index"))


# Home page route
@app.route("/")
def index():
    """Handle homepage route"""
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("homepage.html")


# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle login"""
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
    """Handle registration"""
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


#  Saved movies page route.
@app.route("/movies_saved")
def movies_saved():
    """Handle saved movies route"""
    try:
        if "user_id" not in session:
            flash("Please log in to view saved movies", "error")
            return redirect(url_for("login"))
        saved_predictions = ml_results_collection.find({"user_id": session["user_id"]})
        movies = []
        for prediction in saved_predictions:
            movie = movies_collection.find_one(
                {"title": prediction["results"]["predicted_movie"]}
            )
            movie["sensor_data_id"] = prediction["sensor_data_id"]
            movies.append(movie)
        return render_template("movies_saved.html", movies=movies)
    except OperationFailure:
        flash("Database error occurred", "error")
        logger.error("Database error in movies_saved route")
        return render_template("movies_saved.html", movies=[])


# Logout route
@app.route("/logout")
def logout():
    """Handle logout"""
    session.clear()
    flash("You have been logged out", "success")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("PORT", 5001), debug=True)
