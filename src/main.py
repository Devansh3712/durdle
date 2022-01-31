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
from .database import (
    get_word,
    get_user_streak,
    update_user_streak
)
from .durdle import check_guess
from .utils import (
    create_guess_embed,
    create_final_result_embed,
    create_error_embed,
    update_users_dict,
    get_user_word,
    random_colour
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
client.remove_command("help")

guilds: List[int] = []
users: Dict[str, Dict[str, Any]] = {}
current_word: str = get_word()
english_dictionary = enchant.Dict("en_US")

async def _reset_dict() -> None:
    await client.wait_until_ready()
    while not client.is_closed():
        current_time = datetime.utcnow().strftime("%H%M")
        if current_time == "0000":
            users.clear()
            _time = 86400
        else:
            _time = 1
        await asyncio.sleep(_time)

@client.event
async def on_ready() -> None:
    guilds = [guild for guild in client.guilds]
    print(f"{datetime.utcnow()} - Durdle bot is working")

@client.event
async def on_command_error(ctx, error) -> None:
    pass

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
            embed = create_error_embed("Your 6 guesses are over.")
            return await ctx.send(embed = embed)
        elif users[str(ctx.author)]["guessed"] == True:
            embed = create_error_embed("You have already guessed the word!")
            return await ctx.send(embed = embed)
    if len(word) != 5:
        embed = create_error_embed("Only 5 letter words allowed.")
        return await ctx.send(embed = embed)
    if not english_dictionary.check(word):
        embed = create_error_embed("Word not found in dictionary.")
        return await ctx.send(embed = embed)
    if str(ctx.author) not in users:
        users = get_user_word(ctx, users)
    result = check_guess(word, users[str(ctx.author)]["word"])
    users = update_users_dict(ctx, users, result)
    if users[str(ctx.author)]["count"] == 6:
        update_user_streak(str(ctx.author), False)
        final = create_final_result_embed(ctx, users)
        return await ctx.send(embed = final)
    elif word.lower() == users[str(ctx.author)]["word"]:
        users[str(ctx.author)]["guessed"] = True
        update_user_streak(str(ctx.author), True)
        final = create_final_result_embed(ctx, users)
        return await ctx.send(embed = final)
    embed = create_guess_embed(ctx, users, result)
    return await ctx.send(embed = embed)

@client.command()
async def guess(ctx, word: str):
    global users
    if str(ctx.author) in users:
        if users[str(ctx.author)]["count"] == 6:
            embed = create_error_embed("Your 6 guesses are over.")
            return await ctx.send(embed = embed)
        elif users[str(ctx.author)]["guessed"] == True:
            embed = create_error_embed("You have already guessed the word!")
            return await ctx.send(embed = embed)
    if len(word) != 5:
        embed = create_error_embed("Only 5 letter words allowed.")
        return await ctx.send(embed = embed)
    if not english_dictionary.check(word):
        embed = create_error_embed("Word not found in dictionary.")
        return await ctx.send(embed = embed)
    if str(ctx.author) not in users:
        users = get_user_word(ctx, users)
    result = check_guess(word, users[str(ctx.author)]["word"])
    users = update_users_dict(ctx, users, result)
    if users[str(ctx.author)]["count"] == 6:
        update_user_streak(str(ctx.author), False)
        final = create_final_result_embed(ctx, users)
        return await ctx.send(embed = final)
    elif word.lower() == users[str(ctx.author)]["word"]:
        users[str(ctx.author)]["guessed"] = True
        update_user_streak(str(ctx.author), True)
        final = create_final_result_embed(ctx, users)
        return await ctx.send(embed = final)
    embed = create_guess_embed(ctx, users, result)
    return await ctx.send(embed = embed)

@slash.slash(
    name = "streak",
    description = "Your durdle streak",
    guild_ids = guilds
)
async def _streak(ctx):
    result = get_user_streak(str(ctx.author))
    embed = discord.Embed(
        title = "Durdle Streak",
        colour = random_colour()
    )
    embed.set_thumbnail(url = str(ctx.author.avatar_url))
    embed.add_field(
        name = "Username",
        value = str(ctx.author),
        inline = False
    )
    embed.add_field(
        name = "Max Streak",
        value = f"{result[0]}/{result[1]}",
        inline = False
    )
    percentage = (result[0] / result[1]) * 100 if result[1] else 0
    embed.add_field(
        name = "Accuracy",
        value = f"{percentage:.2f}%",
        inline = False
    )
    return await ctx.send(embed = embed)

@client.command()
async def streak(ctx):
    result = get_user_streak(str(ctx.author))
    embed = discord.Embed(
        title = "Durdle Streak",
        colour = random_colour()
    )
    embed.set_thumbnail(url = str(ctx.author.avatar_url))
    embed.add_field(
        name = "Username",
        value = str(ctx.author),
        inline = False
    )
    embed.add_field(
        name = "Max Streak",
        value = f"{result[0]}/{result[1]}",
        inline = False
    )
    percentage = (result[0] / result[1]) * 100 if result[1] else 0
    embed.add_field(
        name = "Accuracy",
        value = f"{percentage:.2f}%",
        inline = False
    )
    return await ctx.send(embed = embed)

if __name__ == "__main__":
    client.loop.create_task(_reset_dict())
    client.run(token)
