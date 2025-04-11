import csv
from pymongo import MongoClient

client = MongoClient("mongodb://movie_user:movie_password_321@mongodb:27017/")
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
            del row["poster_url"]
            del row["num_ratings"]

          
            collection.insert_one(row)
        except (ValueError, KeyError) as e:
            print(f"Skipping row due to error: {e}")

print("Movies now in MongoDB database.")
