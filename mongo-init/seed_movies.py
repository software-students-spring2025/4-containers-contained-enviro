import csv
from pymongo import MongoClient

client = MongoClient(
    "mongodb://ml_user:ml_password@mongodb:27017/ml_data?authSource=ml_data"
)
db = client["ml_data"]
collection = db["movies"]

collection.delete_many({})

with open("movies.csv", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:

            row["year"] = int(row["year"])
            row["rating"] = float(row["star_rating"])
            del row["star_rating"]

            del row["id"]
            del row["num_ratings"]

            collection.insert_one(row)
        except (ValueError, KeyError) as e:
            print(f"Skipping row due to error: {e}")

print("Movies now in MongoDB database.")
