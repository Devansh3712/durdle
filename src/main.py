from typing import List
from datetime import datetime
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

@client.event
async def on_ready():
    guilds = [guild for guild in client.guilds]
    print(f"{datetime.now()} - Durdle bot is working")

@slash.slash(
    name = "hello",
    description = "Greet the user",
    guild_ids = guilds
)
async def _hello(ctx: SlashContext):
    await ctx.send(f"Hello, {ctx.author.mention}")

client.run(token)
