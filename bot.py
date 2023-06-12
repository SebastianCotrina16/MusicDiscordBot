import os
import discord
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
import yt_dlp as youtube_dl
from Bot.music_bot import MusicBot
from players.player import Player
from players.youtube_player import YouTubePlayer
from players.spotify_player import SpotifyPlayer
from players.tidal_player import TidalPlayer

intents = discord.Intents.all()
intents.members = True
bot = MusicBot(command_prefix=".", self_bot=False,intents=discord.Intents.all())
bot.run(TOKEN)
