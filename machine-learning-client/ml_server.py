"""ML Server sets up flask end-point to allow communication with the web-app"""

import subprocess
import logging
import os
from flask import Flask, request, jsonify
import pandas as pd
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from dotenv import load_dotenv
from ml_client import MLC


# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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


app = Flask(__name__)


def fetch_movies_from_db():
    """Fetch movies from database"""
    db = get_database()
    collection = db["movies"]  # Change to match your collection name
    docs = list(collection.find({}, {"_id": 0, "title": 1, "description": 1}))
    return pd.DataFrame(docs)


@app.route("/recommend", methods=["POST"])
def recommend():
    """Recommend movies endpoint"""
    data = request.get_json()
    user_description = data.get("description", "")
    threshold = float(data.get("threshold", 0.1))

    movie_df = fetch_movies_from_db()

    if movie_df.empty:
        return jsonify({"error": "No movie data found in the database"}), 500

    descriptions = movie_df["description"].tolist()
    ml_client = MLC(descriptions)

    result_df = ml_client.get_recommendations(user_description, movie_df, threshold)

    if isinstance(result_df, str):
        return jsonify({"result": result_df}), 200

    return jsonify(result_df.to_dict(orient="records")), 200


if __name__ == "__main__":
    if os.getenv("GITHUB_ACTIONS") == "true" or os.getenv("CI") == "true":
        logger.info("Detected CI environment — running tests.")
        subprocess.run(["pytest", "test_ml_client.py"], check=True)
    else:
        app.run(host="0.0.0.0", port=6000)
