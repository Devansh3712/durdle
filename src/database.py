from copy import deepcopy
from random import randint
from typing import Tuple
from pymongo import MongoClient
from .config import settings

client = MongoClient(settings.mongodb_uri)
db = client["test"]
word_collection = db["word-list"]
user_collection = db["users"]

def get_word() -> str:
    word_list = list(word_collection.find({}))
    _id = randint(0, len(word_list))
    word = word_list[_id]["word"]
    return word

def update_user_streak(username: str, guessed: bool) -> None:
    user_data = user_collection.find_one({ "username": username })
    if not user_data:
        updated_user_data = {
            "username": username,
            "streak": 0,
            "played": 1
        }
        if guessed:
            updated_user_data["streak"] += 1 # type: ignore
        user_collection.insert_one(updated_user_data)
    else:
        updated_user_data = deepcopy(user_data)
        if guessed:
            updated_user_data["streak"] += 1 # type: ignore
        else:
            updated_user_data["streak"] = 0
        updated_user_data["played"] += 1 # type: ignore
        user_collection.update_one(
            user_data,
            { "$set": updated_user_data },
            upsert = False
        )

def get_user_streak(username: str) -> Tuple[int, int]:
    user_data = user_collection.find_one({ "username": username })
    if not user_data:
        updated_user_data = {
            "username": username,
            "streak": 0,
            "played": 0
        }
        user_collection.insert_one(updated_user_data)
        return (0, 0)
    else:
        return (user_data["streak"], user_data["played"])
