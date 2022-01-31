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
from spellchecker import SpellChecker
from src.config import settings
from src.database import (
    get_user_streak,
    update_user_streak
)
from src.durdle import check_guess
from src.utils import (
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
spell_checker = SpellChecker()
english_dictionary = lambda word: word == spell_checker.correction(word)

async def _reset_dict() -> None:
    """Clear the global users dictionary at 0000 hours GMT"""
    global users
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
    """Generate a list of guilds of durdle bot"""
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
    """Guess a 5 letter word in 6 tries. Different word
    is generated for every user.

    A dictionary is created for every user with the following
    schema:

    {
        "word": get_word(),
        "count": 0,
        "tries": [],
        "guessed": False
    }
    
    If the user guesses the word under 6 guesses, their durdle
    streak in database gets incremented by 1 else the streak becomes
    0.

    Args:
        word (str): Word guessed by the user.
    """
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
    if not english_dictionary(word):
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
    if not english_dictionary(word):
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
    """Fetch current user's maximum durdle streak from
    the database"""
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

@slash.slash(
    name = "help",
    description = "Durdle commands",
    guild_ids = guilds
)
async def _help(ctx):
    """Returns an embed with all commands of Durdle bot"""
    embed = discord.Embed(
        title = "Durdle Commands",
        colour = random_colour()
    )
    embed.set_thumbnail(url = str(client.user.avatar_url))
    embed.add_field(
        name = "Guess today's word",
        value = "`/guess`"
    )
    embed.add_field(
        name = "Get your max durdle streak",
        value = "`/streak`"
    )
    embed.add_field(
        name = "Information about durdle bot",
        value = "`/info`"
    )
    return await ctx.send(embed = embed)

@client.command()
async def help(ctx):
    embed = discord.Embed(
        title = "Durdle Commands",
        colour = random_colour()
    )
    embed.set_thumbnail(url = str(client.user.avatar_url))
    embed.add_field(
        name = "Guess today's word",
        value = "`/guess`"
    )
    embed.add_field(
        name = "Get your max durdle streak",
        value = "`/streak`"
    )
    return await ctx.send(embed = embed)

@slash.slash(
    name = "info",
    description = "Durdle bot information",
    guild_ids = guilds
)
async def _info(ctx):
    """Returns an embed with information about Durdle bot"""
    embed = discord.Embed(
        title = "Durdle Information",
        colour = random_colour(),
        description = "Durdle is a Discord bot inspired by the popular internet game [Wordle](https://powerlanguage.co.uk/wordle/)."
    )
    embed.set_thumbnail(url = str(client.user.avatar_url))
    embed.add_field(
        name = "How to play",
        value = "Each player has six tries to guess a target five-letter word. A new word is generated for every user each day.",
        inline = False
    )
    embed.add_field(
        name = "Creators",
        value = "[Devansh Singh](https://github.com/Devansh3712), [Kshitij Kapoor](https://github.com/kshitijk4poor)",
        inline = False
    )
    embed.add_field(
        name = "Made with",
        value = "Python, MongoDB, Heroku",
        inline = False
    )
    features = [
        "• Different word for every user",
        "• Word resets at 0000 hours GMT",
        "• Provides the meaning and usasge of the word (if found on [Word API](https://dictionaryapi.dev/))",
        "• Keeps count of durdle play streak of every user"
    ]
    embed.add_field(
        name = "Features",
        value = "\n".join(features),
        inline = False
    )
    return await ctx.send(embed = embed)

@client.command()
async def info(ctx):
    embed = discord.Embed(
        title = "Durdle Information",
        colour = random_colour(),
        description = "Durdle is a Discord bot inspired by the popular internet game [Wordle](https://powerlanguage.co.uk/wordle/)."
    )
    embed.set_thumbnail(url = str(client.user.avatar_url))
    embed.add_field(
        name = "How to play",
        value = "Each player has six tries to guess a target five-letter word. A new word is generated for every user each day.",
        inline = False
    )
    embed.add_field(
        name = "Creators",
        value = "[Devansh Singh](https://github.com/Devansh3712), [Kshitij Kapoor](https://github.com/kshitijk4poor)",
        inline = False
    )
    embed.add_field(
        name = "Made with",
        value = "Python, MongoDB, Heroku",
        inline = False
    )
    features = [
        "• Different word for every user",
        "• Word resets at 0000 hours GMT",
        "• Provides the meaning and usasge of the word (if found on [Word API](https://dictionaryapi.dev/))",
        "• Keeps count of durdle play streak of every user"
    ]
    embed.add_field(
        name = "Features",
        value = "\n".join(features),
        inline = False
    )

if __name__ == "__main__":
    client.loop.create_task(_reset_dict())
    client.run(token)
