from typing import (
    Any,
    Dict,
    List
)
from datetime import datetime
import asyncio
import discord
from discord.ext import commands
from discord_slash import (
    SlashCommand,
    SlashContext
)
from discord_slash.utils.manage_commands import (
    create_choice,
    create_option
)
import enchant
from .config import settings
from .database import get_word
from .durdle import check_guess
from .utils import (
    create_guess_embed,
    create_final_result_embed,
    create_error_embed,
    update_users_dict
)

token = settings.token
client = commands.Bot(
    command_prefix = "$d ",
    activity = discord.Activity(
        type = discord.ActivityType.playing,
        name = "wordle"
    )
)
slash = SlashCommand(client, sync_commands = True)

guilds: List[int] = []
users: Dict[str, Dict[str, Any]] = {}
current_word: str = get_word()
english_dictionary = enchant.Dict("en_US")
print(datetime.utcnow().strftime("%d %B, %Y"), ": ", current_word)

async def _current_word() -> None:
    await client.wait_until_ready()
    while not client.is_closed():
        global current_word
        current_time = datetime.utcnow().strftime("%H%M")
        if current_time == "0000":
            current_word = get_word()
            users.clear()
            current_date = datetime.utcnow().strftime("%d %B, %Y")
            print(f"{current_date}: {current_word}")
            _time = 86400
        else:
            _time = 1
        await asyncio.sleep(_time)

@client.event
async def on_ready() -> None:
    guilds = [guild for guild in client.guilds]
    print(f"{datetime.utcnow()} - Durdle bot is working")

@slash.slash(
    name = "guess",
    description = "Guess today's word",
    guild_ids = guilds,
    options = [
        create_option(
            name = "word",
            description = "Enter the word",
            option_type = 3,
            required = True
        )
    ]
)
async def _guess(ctx, word: str):
    global users
    if str(ctx.author) in users:
        if users[str(ctx.author)]["count"] == 6:
            embed = create_error_embed(ctx, "Your 6 guesses are over.")
            return await ctx.send(embed = embed)
        elif users[str(ctx.author)]["guessed"] == True:
            embed = create_error_embed(ctx, "You have already guessed the word!")
            return await ctx.send(embed = embed)
    if len(word) != 5:
        embed = create_error_embed(ctx, "Only 5 letter words allowed.")
        return await ctx.send(embed = embed)
    if not english_dictionary.check(word):
        embed = create_error_embed(ctx, "Word not found in dictionary.")
        return await ctx.send(embed = embed)
    result = check_guess(word, current_word)
    users = update_users_dict(ctx, users, result)
    if users[str(ctx.author)]["count"] == 6:
        final = create_final_result_embed(ctx, users)
        return await ctx.send(embed = final)
    elif word.lower() == current_word:
        users[str(ctx.author)]["guessed"] = True
        final = create_final_result_embed(ctx, users)
        return await ctx.send(embed = final)
    embed = create_guess_embed(ctx, users, result)
    return await ctx.send(embed = embed)

@client.command()
async def guess(ctx, word: str):
    global users
    if str(ctx.author) in users:
        if users[str(ctx.author)]["count"] == 6:
            embed = create_error_embed(ctx, "Your 6 guesses are over.")
            return await ctx.send(embed = embed)
        elif users[str(ctx.author)]["guessed"] == True:
            embed = create_error_embed(ctx, "You have already guessed the word!")
            return await ctx.send(embed = embed)
    if len(word) != 5:
        embed = create_error_embed(ctx, "Only 5 letter words allowed.")
        return await ctx.send(embed = embed)
    if not english_dictionary.check(word):
        embed = create_error_embed(ctx, "Word not found in dictionary.")
        return await ctx.send(embed = embed)
    result = check_guess(word, current_word)
    users = update_users_dict(ctx, users, result)
    if users[str(ctx.author)]["count"] == 6:
        final = create_final_result_embed(ctx, users)
        return await ctx.send(embed = final)
    elif word.lower() == current_word:
        users[str(ctx.author)]["guessed"] = True
        final = create_final_result_embed(ctx, users)
        return await ctx.send(embed = final)
    embed = create_guess_embed(ctx, users, result)
    return await ctx.send(embed = embed)

if __name__ == "__main__":
    client.loop.create_task(_current_word())
    client.run(token)
