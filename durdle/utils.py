# type: ignore[import]

__author__ = "Devansh Singh"
__license__ = "GNU AGPLv3"
__version__ = "0.1.0"
__status__ = "Development"

from datetime import datetime
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Tuple,
)
from urllib.parse import quote_plus
import random
import discord
from discord.commands.context import ApplicationContext
from discord.ui import (
    Button,
    View,
)
from .database import (
    get_user_streak,
    get_word,
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
    ctx: ApplicationContext,
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
    embed.set_thumbnail(url = str(ctx.author.display_avatar))
    return embed

def create_final_result_embed(
    ctx: ApplicationContext,
    users: Dict[str, Dict[str, Any]],
    count: int
) -> discord.Embed:
    """If user's guess is correct, durdle bot returns the
    final embed with all tries of the user and the maximum
    streak.

    Args:
        users (Dict[str, Dict[str, Any]]): Dictionary of users data.
        count (int): Durdle day counter.
    """
    streaks: Tuple[int, ...] = get_user_streak(str(ctx.author))
    meaning: str = users[str(ctx.author)]["meaning"]
    usage: str = users[str(ctx.author)]["usage"]
    embed = discord.Embed(
        title = "\n".join(users[str(ctx.author)]["tries"]),
        colour = discord.Colour.green(),
        description = f"**Durdle {count} {users[str(ctx.author)]['count']}/6**"
    )
    embed.add_field(
        name = "Word", value = users[str(ctx.author)]["word"]
    )
    embed.add_field(
        name = "Max Streak", value = f"{streaks[0]}/{streaks[1]}"
    )
    if (meaning):
        embed.add_field(
            name = "Meaning", value = meaning, inline = False
        )
    if (usage):
        embed.add_field(
            name = "Usage", value = usage, inline = False
        )
    embed.set_thumbnail(url = str(ctx.author.display_avatar))
    return embed

def create_final_result_view(
    ctx: ApplicationContext,
    users: Dict[str, Dict[str, Any]],
    count: int
) -> discord.ui.View:
    """Return a view with copy result and share to Twitter
    button for the final result embed.

    Args:
        users (Dict[str, Dict[str, Any]]): Dictionary of users data.
        count (int): Durdle day counter.
    """
    tries: str = "\n".join(users[str(ctx.author)]["tries"])
    count: str = f"Durdle {count} {users[str(ctx.author)]['count']}/6\n"
    share: str = count + tries.replace(" ", "")
    twitter = Button(
        label = "Share on Twitter",
        style = discord.ButtonStyle.primary,
        url = f"http://twitter.com/share?text={quote_plus(share)}"
    )
    view = View()
    view.add_item(twitter)
    return view

def create_error_embed(error: str) -> discord.Embed:
    embed = discord.Embed(
        title = f"⛔ {error}", colour = discord.Colour.red()
    )
    return embed

def update_users_dict(
    ctx: ApplicationContext,
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
    ctx: ApplicationContext,
    users: Dict[str, Dict[str, Any]]
) -> Dict[str, Dict[str, Any]]:
    """Fetch a new word for every user from the durdle word
    list.

    Args:
        users (Dict[str, Dict[str, Any]]): Dictionary of user's data.

    Returns:
        Dict[str, Dict[str, Any]]: Updated dictionary of user's data.
    """
    if (str(ctx.author) not in users):
        word: Tuple[str, ...] = get_word()
        users[str(ctx.author)]: Dict[str, Any] = {
            "word": word[0],
            "meaning": word[1],
            "usage": word[2],
            "count": 0,
            "tries": [],
            "guessed": False,
        }
    return users
