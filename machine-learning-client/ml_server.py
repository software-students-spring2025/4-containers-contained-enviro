"""ML Server sets up flask end-point to allow communication with the web-app"""

import logging
import os
from flask import Flask, request, jsonify
import pandas as pd
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from dotenv import load_dotenv
from ml_client import MLC
from datetime import datetime
from bson.json_util import dumps

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


@app.route("/process_pending", methods=["POST"])
def process_pending():
    db = get_database()
    sensor_collection = db["sensor_data"]
    results_collection = db["ml_results"]

    # Find all recordings with status pending.
    pending_docs = list(sensor_collection.find({"status": "pending"}))
    if not pending_docs:
        return jsonify({"message": "No pending recordings."}), 200

    predictions = []

    for doc in pending_docs:
        recording_id = doc["_id"]
        user_id = doc["user_id"]

        # TODO: convert audio_data into text
        audio_data = doc["raw_data"]

        # TODO: run model below on the text

        predicted_movie = "Inception"
        confidence = 0.95

        """
        user_description = data.get("description", "")
        threshold = float(data.get("threshold", 0.1))

        movie_df = fetch_movies_from_db()

        if movie_df.empty:
            return jsonify({"error": "No movie data found in the database"}), 500

        descriptions = movie_df["description"].tolist()
        ml_client = MLC(descriptions)

        result_df = ml_client.get_recommendations(user_description, movie_df, threshold)
        """

        prediction = {
            "timestamp": datetime.now(),
            "sensor_data_id": recording_id,
            "model_type": "default",
            "results": {
                "predicted_movie": predicted_movie,
                "confidence": confidence,
            },
            "user_id": user_id,
        }
        results_collection.insert_one(prediction)
        sensor_collection.update_one(
            {"_id": recording_id}, {"$set": {"status": "processed"}}
        )
        prediction["recording_id"] = str(recording_id)
        predictions.append(prediction)

    response_json = dumps({"processed": len(predictions), "predictions": predictions})
    return response_json, 200, {"Content-Type": "application/json"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
