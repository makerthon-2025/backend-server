from pymongo import MongoClient
import os
from src.helper import env_load_helper

env_load_helper.load_env()

client = MongoClient(f"mongodb+srv://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PASSWD')}@{os.getenv('MONGO_HOST')}/{os.getenv('MONGO_DB')}?retryWrites=true&w=majority")

db = client[os.getenv('MONGO_DB')]

collection = db['news']

def insert_collection(data):
    id = collection.insert_one(data).inserted_id
    return id

def delete_collection(id):
    result = collection.delete_one({"_id": id})
    return result.deleted_count

def get_collection(_id):
    result = collection.find_one({"_id": _id})
    return result

def get_collection_by_name(name):
    result = collection.find_one({"name": name})
    return result

def update_collection(data):
    result = collection.update_one({"name": data['name']}, {"$set": data})
    return True


