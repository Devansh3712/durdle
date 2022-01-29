from typing import List
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
from .config import settings
from .database import get_word

token = settings.token
client = commands.Bot(
    command_prefix = "$",
    activity = discord.Activity(
        type = discord.ActivityType.playing,
        name = "wordle"
    )
)
slash = SlashCommand(client, sync_commands = True)
guilds: List[int] = []
current_word: str = get_word()

async def _current_word():
    await client.wait_until_ready()
    while not client.is_closed():
        global current_word
        current_time = datetime.utcnow().strftime("%H%M")
        if current_time == "0000":
            current_word = get_word()
            _time = 86400
        else:
            _time = 1
        await asyncio.sleep(_time)

@client.event
async def on_ready():
    guilds = [guild for guild in client.guilds]
    print(f"{datetime.utcnow()} - Durdle bot is working")

@slash.slash(
    name = "hello",
    description = "Greet the user",
    guild_ids = guilds
)
async def _hello(ctx: SlashContext):
    await ctx.send(f"Hello, {ctx.author.mention}")

@slash.slash(
    name = "word",
    description = "Get a today's word",
    guild_ids = guilds
)
async def _word(ctx):
    await ctx.send(f"Today's word is: {current_word}")

if __name__ == "__main__":
    client.loop.create_task(_current_word())
    client.run(token)
