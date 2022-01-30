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

def random_colour() -> int:
	rgb: Callable[[], int] = lambda: random.randint(0, 255)
	colour: str = "%02X%02X%02X" % (rgb(), rgb(), rgb())
	return int(colour, 16)

def create_guess_embed(
    ctx,
    users: Dict[str, Dict[str, Any]],
    result: Tuple[str, str]
) -> discord.Embed:
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
    embed = discord.Embed(
        title = "\n".join(users[str(ctx.author)]["tries"]),
        colour = discord.Colour.green(),
        description = f"**Durdle {users[str(ctx.author)]['count']}/6**"
    )
    embed.set_thumbnail(url = str(ctx.author.avatar_url))
    return embed

def create_error_embed(ctx, error: str) -> discord.Embed:
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
    if str(ctx.author) in users:
        users[str(ctx.author)]["count"] += 1
        users[str(ctx.author)]["tries"].append(result[0])
    else:
        users[str(ctx.author)] = {}
        users[str(ctx.author)]["count"] = 1
        users[str(ctx.author)]["tries"] = [result[0]]
        users[str(ctx.author)]["guessed"] = False
    return users
