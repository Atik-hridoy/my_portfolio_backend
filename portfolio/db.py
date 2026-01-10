import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB URI
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["portfolio_db"]  # Database name: portfolio_db

# Centralized collections
projects_collection = db["projects"]
contacts_collection = db["contacts"]
