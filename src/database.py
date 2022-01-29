from random import randint
from pymongo import MongoClient
from .config import settings

client = MongoClient(settings.mongodb_uri)
db = client["test"]
collection = db["word-list"]

def get_word() -> str:
    word_list = list(collection.find({}))
    _id = randint(0, len(word_list))
    word = word_list[_id]["word"]
    return word
