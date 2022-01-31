from datetime import datetime
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Tuple
)
import random
import discord
from .database import (
    get_user_streak,
    get_word
)

def random_colour() -> int:
    """Generates a random hex colour code.

    Returns:
        int: Hex code of the colour generated.
    """
    rgb: Callable[[], int] = lambda: random.randint(0, 255)
    colour: str = "%02X%02X%02X" % (rgb(), rgb(), rgb())
    return int(colour, 16)

def create_guess_embed(
    ctx,
    users: Dict[str, Dict[str, Any]],
    result: Tuple[str, str]
) -> discord.Embed:
    """If user's guess is not correct, durdle bot returns
    the guess embed of the word.

    Args:
        users (Dict[str, Dict[str, Any]]): Dictionary of users data.
        result (Tuple[str, str]): Result of guessed word and actual
        word's comparison.
    """
    embed = discord.Embed(
        title = result[0] + "\n" + result[1],
        colour = random_colour(),
        description = f"**Durdle {users[str(ctx.author)]['count']}/6**"
    )
    embed.set_thumbnail(url = str(ctx.author.avatar_url))
    return embed

def create_final_result_embed(
    ctx,
    users: Dict[str, Dict[str, Any]]
) -> discord.Embed:
    """If user's guess is correct, durdle bot returns the
    final embed with all tries of the user and the maximum
    streak.

    Args:
        users (Dict[str, Dict[str, Any]]): Dictionary of users data.
    """
    streaks = get_user_streak(str(ctx.author))
    embed = discord.Embed(
        title = "\n".join(users[str(ctx.author)]["tries"]),
        colour = discord.Colour.green(),
        description = f"**Durdle {users[str(ctx.author)]['count']}/6**"
    )
    embed.add_field(
        name = "Word",
        value = users[str(ctx.author)]["word"]
    )
    embed.add_field(
        name = "Max Streak",
        value = f"{streaks[0]}/{streaks[1]}"
    )
    embed.set_thumbnail(url = str(ctx.author.avatar_url))
    return embed

def create_error_embed(error: str) -> discord.Embed:
    embed = discord.Embed(
        title = f"⛔ {error}",
        colour = discord.Colour.red()
    )
    return embed

def update_users_dict(
    ctx,
    users: Dict[str, Dict[str, Any]],
    result: Tuple[str, str]
) -> Dict[str, Dict[str, Any]]:
    """Update a user's dictionary values in the global users
    dictionary.

    Args:
        users (Dict[str, Dict[str, Any]]): Dictionary of user's data.
        result (Tuple[str, str]): Result of guessed word and actual
        word's comparison.

    Returns:
        Dict[str, Dict[str, Any]]: Updated dictionary of user's data.
    """
    users[str(ctx.author)]["count"] += 1
    users[str(ctx.author)]["tries"].append(result[0])
    return users

def get_user_word(
    ctx,
    users: Dict[str, Dict[str, Any]]
) -> Dict[str, Dict[str, Any]]:
    """Fetch a new word for every user from the durdle word
    list.

    Args:
        users (Dict[str, Dict[str, Any]]): Dictionary of user's data.

    Returns:
        Dict[str, Dict[str, Any]]: Updated dictionary of user's data.
    """
    if str(ctx.author) not in users:
        users[str(ctx.author)] = {
            "word": get_word(),
            "count": 0,
            "tries": [],
            "guessed": False
        }
    return users
