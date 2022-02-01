from typing import (
    Any,
    Dict,
    List
)
from datetime import datetime
import asyncio
import discord
from discord.commands import slash_command
from discord.ext import commands
from discord.ui import (
    Button,
    View
)
from spellchecker import SpellChecker
from durdle.config import settings
from durdle.database import (
    get_user_streak,
    update_user_streak
)
from durdle.durdle import check_guess
from durdle.utils import (
    create_guess_embed,
    create_final_result_embed,
    create_error_embed,
    update_users_dict,
    get_user_word,
    random_colour
)

token = settings.token
client = commands.Bot()
client.help_command = None

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
    print(f"{datetime.utcnow()} - Durdle bot is working")

@client.event
async def on_command_error(ctx, error) -> None:
    pass

@client.slash_command(
    name = "guess",
    description = "Guess today's word"
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
            await ctx.respond(embed = embed)
        elif users[str(ctx.author)]["guessed"] == True:
            embed = create_error_embed("You have already guessed the word!")
            await ctx.respond(embed = embed)
        elif len(word) != 5:
            embed = create_error_embed("Only 5 letter words allowed.")
            await ctx.respond(embed = embed)
        elif not english_dictionary(word) and word != users[str(ctx.author)]["word"]:
            embed = create_error_embed("Word not found in dictionary.")
            await ctx.respond(embed = embed)
        else:
            result = check_guess(word, users[str(ctx.author)]["word"])
            users = update_users_dict(ctx, users, result)
            if users[str(ctx.author)]["count"] == 6:
                update_user_streak(str(ctx.author), False)
                final = create_final_result_embed(ctx, users)
                await ctx.respond(embed = final)
            elif word.lower() == users[str(ctx.author)]["word"]:
                users[str(ctx.author)]["guessed"] = True
                update_user_streak(str(ctx.author), True)
                final = create_final_result_embed(ctx, users)
                await ctx.respond(embed = final)
            else:
                embed = create_guess_embed(ctx, users, result)
                await ctx.respond(embed = embed)
    else:
        if len(word) != 5:
            embed = create_error_embed("Only 5 letter words allowed.")
            await ctx.respond(embed = embed)
        elif not english_dictionary(word):
            embed = create_error_embed("Word not found in dictionary.")
            await ctx.respond(embed = embed)
        else:
            users = get_user_word(ctx, users)
            result = check_guess(word, users[str(ctx.author)]["word"])
            users = update_users_dict(ctx, users, result)
            if users[str(ctx.author)]["count"] == 6:
                update_user_streak(str(ctx.author), False)
                final = create_final_result_embed(ctx, users)
                await ctx.respond(embed = final)
            elif word.lower() == users[str(ctx.author)]["word"]:
                users[str(ctx.author)]["guessed"] = True
                update_user_streak(str(ctx.author), True)
                final = create_final_result_embed(ctx, users)
                await ctx.respond(embed = final)
            else:
                embed = create_guess_embed(ctx, users, result)
                await ctx.respond(embed = embed)

@client.slash_command(
    name = "streak",
    description = "Your durdle streak"
)
async def _streak(ctx):
    """Fetch current user's maximum durdle streak from
    the database"""
    result = get_user_streak(str(ctx.author))
    embed = discord.Embed(
        title = "Durdle Streak",
        colour = random_colour()
    )
    embed.set_thumbnail(url = str(ctx.author.display_avatar))
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
    await ctx.respond(embed = embed)

@client.slash_command(
    name = "help",
    description = "Durdle commands"
)
async def _help(ctx):
    """Returns an embed with all commands of Durdle bot"""
    embed = discord.Embed(
        title = "Durdle Commands",
        colour = random_colour()
    )
    embed.set_thumbnail(url = str(client.user.display_avatar))
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
    await ctx.respond(embed = embed)

@client.slash_command(
    name = "info",
    description = "Durdle bot information"
)
async def _info(ctx):
    """Returns an embed with information about Durdle bot"""
    embed = discord.Embed(
        title = "Durdle Information",
        colour = random_colour(),
        description = "Durdle is a Discord bot inspired by the popular internet game [Wordle](https://powerlanguage.co.uk/wordle/)."
    )
    embed.set_thumbnail(url = str(client.user.display_avatar))
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
    website = Button(
        label = "Website",
        url = r"https://kshitijk4poor.github.io/durdle-website/"
    )
    bot_link = Button(
        label = "Add to another server",
        url = r"https://discord.com/oauth2/authorize?client_id=936880656938594334&permissions=8&scope=bot%20applications.commands"
    )
    view = View()
    view.add_item(website)
    view.add_item(bot_link)
    await ctx.respond(embed = embed, view = view)

if __name__ == "__main__":
    client.loop.create_task(_reset_dict())
    client.run(token)
