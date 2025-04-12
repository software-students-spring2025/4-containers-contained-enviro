"""Tests for basic user and movie document operations in the database."""

from pymongo import MongoClient
from bson.objectid import ObjectId

def test_user_insertion_and_retrieval():
    """Insert a test user and verify retrieval from database."""
    client = MongoClient("mongodb://localhost:27017/")
    db = client["ml_data"]
    user = {"username": "test_user_123", "password": "pass123", "saved_movies": []}
    inserted = db.users.insert_one(user)
    found = db.users.find_one({"_id": inserted.inserted_id})
    assert found is not None
    assert found["username"] == "test_user_123"
    db.users.delete_one({"_id": ObjectId(inserted.inserted_id)})


def test_movie_lookup():
    """Verify a known movie exists (seeded movie)."""
    client = MongoClient("mongodb://localhost:27017/")
    db = client["ml_data"]
    movie = db.movies.find_one()
    assert movie is not None
    assert "title" in movie
