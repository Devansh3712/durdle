from datetime import datetime
import discord
from discord.ext import commands
from .config import settings

client = commands.Bot(
    command_prefix = "$",
    activity = discord.Activity(
        type = discord.ActivityType.playing,
        name = "wordle"
    )
)
token = settings.token

@client.event
async def on_ready():
    print(f"{datetime.now()} - Durdle bot is working")

client.run(token)
