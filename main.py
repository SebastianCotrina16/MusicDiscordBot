from dotenv import load_dotenv
import os
from bot import MusicBot
import discord

load_dotenv()

COMMAND_PREFIX = '.'
intents = discord.Intents.all()

TOKEN = os.getenv('TOKEN')

bot = MusicBot(command_prefix=COMMAND_PREFIX, intents=intents)

@bot.event
async def on_ready():
    print('Bot online')
    print('Comandos registrados:')
    for command in bot.commands:
        print(command.name)

bot.run(TOKEN)
