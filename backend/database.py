from pymongo import MongoClient 
from dotenv import load_dotenv 
import os 
 
load_dotenv() 
 
client = MongoClient(os.getenv("MONGO_URI")) 
db = client["taskdb"] 
 
users_collection = db["users"] 
tasks_collection = db["tasks"] 
 
