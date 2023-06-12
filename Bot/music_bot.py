import asyncio
import discord
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
import yt_dlp as youtube_dl
from players.player import Player
from players.spotify_player import SpotifyPlayer
from players.youtube_player import YouTubePlayer
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'quiet': True,
}

class MusicBot(commands.Bot):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MusicBot, cls).__new__(cls)
        return cls._instance

    def __init__(self, command_prefix, self_bot,intents):
        commands.Bot.__init__(self, command_prefix=command_prefix, self_bot=self_bot,intents=intents)
        self.add_commands()

    async def on_ready(self):
        print('Bot Online')
    def add_commands(self):
        @self.command(name="join",pass_context=True)
        async def join(ctx):
            if ctx.author.voice is None:
                await ctx.send("You are not connected to a voice channel!")
                return
            channel = ctx.author.voice.channel
            voice = get(self.voice_clients, guild=ctx.guild)
            if voice and voice.is_connected():
                await voice.move_to(channel)
            else:
                voice = await channel.connect()
        @self.command(name="play",pass_context=True)
        async def play(ctx, *, query):
            if ctx.author.voice is None:
                await ctx.send("You are not connected to a voice channel!")
                return
            channel = ctx.author.voice.channel
            voice_client = ctx.guild.voice_client
            if voice_client is None or not voice_client.is_connected():
                voice_client = await channel.connect()
            if voice_client.is_playing():
                voice_client.stop()

            player = None
            song_url = None
            if "youtube.com" in query:
                player = YouTubePlayer()
                song_url = query
            elif "spotify.com" in query:
                player = SpotifyPlayer()
                track_id = query.split('/')[-1].split('?')[0]  # Extract the track ID from the Spotify URL
                song_query = player.play(track_id)  # Get the artist name and song title from Spotify
                youtube_player = YouTubePlayer()
                song_url = youtube_player.play(song_query)
            else:
                player = YouTubePlayer()
                song_url = player.play(query)

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(song_url, download=False)
                best_audio = max(info["formats"], key=lambda f: f.get("abr", 0))
                audio_url = best_audio["url"]
            FFMPEG_OPTIONS = {
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                'options': '-vn',
            }
            voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=audio_url, **FFMPEG_OPTIONS))
        @self.command(name="resume",pass_context=True)
        async def resume(self, ctx):
            voice = get(self.voice_clients, guild=ctx.guild)

            if not voice.is_playing():
                voice.resume()
                await ctx.send('Resumiendo')
        @self.command(name="pause",pass_context=True)
        async def pause(self, ctx):
            voice = get(self.voice_clients, guild=ctx.guild)

            if voice.is_playing():
                voice.pause()
                await ctx.send('Stop')
        @self.command(name="Stop",pass_context=True)
        async def stop(self, ctx):
            voice = get(self.voice_clients, guild=ctx.guild)

            if voice.is_playing():
                voice.stop()
                await ctx.send('Parando')