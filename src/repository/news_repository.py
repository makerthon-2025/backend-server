from pymongo import MongoClient
from bson import ObjectId
import os
from src.helper import env_load_helper

env_load_helper.load_env()

client = MongoClient(f"mongodb+srv://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PASSWD')}@{os.getenv('MONGO_HOST')}/{os.getenv('MONGO_DB')}?retryWrites=true&w=majority")

db = client[os.getenv('MONGO_DB')]

collection = db['news']

def update_collection(data):
    result = collection.update_one({"name": data['name']}, {"$set": data})
    return True

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

def get_top_n_by_count(type_value, limit):
    results = collection.find({"type": type_value}).sort([
        ("type", 1),        # Sắp xếp type tăng dần (ở đây cùng 1 type thì không ảnh hưởng)
        ("count", -1),      # count giảm dần
        ("date", -1)        # ngày mới trước
    ]).limit(limit)

    list_results = []
    for doc in results:
        if "_id" in doc and isinstance(doc["_id"], ObjectId):
            doc["_id"] = str(doc["_id"])
        list_results.append(doc)
    return list_results



