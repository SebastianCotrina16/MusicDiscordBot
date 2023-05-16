from dotenv import load_dotenv
import os
from bot import MusicBot
import discord

load_dotenv()

TOKEN = os.getenv('TOKEN')
COMMAND_PREFIX = "."
intents = discord.Intents.all()
intents.members = True

bot = MusicBot(command_prefix=COMMAND_PREFIX, intents=intents)
bot.run(TOKEN)
