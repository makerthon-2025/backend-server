from pymongo import MongoClient
import os
from src.helper import env_load_helper

env_load_helper.load_env()

client = MongoClient(f'mongodb://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PASSWD')}@{os.getenv('MONGO_HOST')}:{os.getenv('MONGO_PORT')}/')

db = client[os.getenv('MONGO_DB')]

collection = db[os.getenv['MONGO_COLLECTION_NAME']]

def insert_collection(data):
    id = collection.insert_one(data).inserted_id
    return id


