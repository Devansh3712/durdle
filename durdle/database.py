__author__ = "Devansh Singh"
__license__ = "GNU AGPLv3"
__version__ = "0.1.0"
__status__ = "Development"

from copy import deepcopy
from random import randint
from typing import Tuple
from pymongo import MongoClient
from .config import settings
from .dictionary import word_list

client = MongoClient(settings.mongodb_uri)
db = client["durdle"]
user_collection = db["users"]

def get_word() -> Tuple[str, ...]:
    """Fetch a random word, its meaning and usage from
    the word list declared in the dictionary file.

    Returns:
        Tuple[str, ...]: Word, its meaning and usage fetched from
        the dictionary file.
    """
    _id = randint(0, len(word_list))
    word_data: Tuple[str, ...] = (
        word_list[_id]["word"],
        word_list[_id]["meaning"].decode("utf-8"),
        word_list[_id]["usage"].decode("utf-8")
    )
    return word_data

def update_user_streak(username: str, guessed: bool) -> None:
    """Update a user's streak in the durdle database.
    Increments the current streak by 1 if user guessed the
    word else set to 0.
    
    Maximum streak is the max(current_streak, max_streak).
    The document schema for a user is as follows:
    
    {
        "username": username,
        "current_streak": 0,
        "max_streak": 0,
        "played": 0
    }

    Args:
        username (str): User whose data has to be updated.
        guessed (bool): Whether the user was able to guess the word or not.
    """
    user_data = user_collection.find_one({ "username": username })
    if not user_data:
        updated_user_data = {
            "username": username,
            "current_streak": 0,
            "max_streak": 0,
            "played": 0
        }
        if guessed:
            updated_user_data["current_streak"] += 1 # type: ignore
        else:
            updated_user_data["current_streak"] = 0
        updated_user_data["played"] += 1 # type: ignore
        if updated_user_data["current_streak"] > updated_user_data["max_streak"]: # type: ignore
            updated_user_data["max_streak"] = updated_user_data["current_streak"]
        user_collection.insert_one(updated_user_data)
    else:
        updated_user_data = deepcopy(user_data)
        if guessed:
            updated_user_data["current_streak"] += 1 # type: ignore
        else:
            updated_user_data["current_streak"] = 0
        updated_user_data["played"] += 1 # type: ignore
        if updated_user_data["current_streak"] > updated_user_data["max_streak"]: # type: ignore
            updated_user_data["max_streak"] = updated_user_data["current_streak"]
        user_collection.update_one(
            user_data,
            { "$set": updated_user_data },
            upsert = False
        )

def get_user_streak(username: str) -> Tuple[int, int]:
    """Fetch a user's maximum streak from the database
    if it exists else create a user document.

    Args:
        username (str): User whose streak has to be fetched.

    Returns:
        Tuple[int, int]: Tuple of maximum streak and number of
        times they played durdle.
    """
    user_data = user_collection.find_one({ "username": username })
    if not user_data:
        updated_user_data = {
            "username": username,
            "current_streak": 0,
            "max_streak": 0,
            "played": 0
        }
        user_collection.insert_one(updated_user_data)
        return (0, 0)
    else:
        return (user_data["max_streak"], user_data["played"])
