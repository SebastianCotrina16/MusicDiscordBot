import asyncio
import discord
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
import yt_dlp as youtube_dl

INACTIVITY_TIME = 120
AUDIO_FORMAT_OPTIONS = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'quiet': True,
}
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}

class MusicBot(commands.Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix, intents=intents)

    async def on_ready(self):
        print('Bot online')
        print('Comandos registrados:')
        for command in self.commands:
            print(command.name)

    async def disconnect_after_inactivity(self, voice_client):
        await asyncio.sleep(INACTIVITY_TIME)
        if not voice_client.is_playing() and not voice_client.is_paused():
            await voice_client.disconnect()

    @commands.command()    
    async def join(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

    @commands.command()
    async def play(self, ctx, *, url):
        await self.join(ctx)
        voice_client = ctx.guild.voice_client
        if voice_client.is_playing():
            voice_client.stop()
        with youtube_dl.YoutubeDL(AUDIO_FORMAT_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            if "formats" not in info:
                return await ctx.send("No se pudo obtener la información del formato del video.")
            best_audio = max(info["formats"], key=lambda f: f.get("abr", 0))
            audio_url = best_audio["url"]
        voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=audio_url, **FFMPEG_OPTIONS))
        asyncio.create_task(self.disconnect_after_inactivity(voice_client))

    @commands.command()
    async def resume(self, ctx):
        voice = get(self.voice_clients, guild=ctx.guild)
        if not voice.is_playing():
            voice.resume()
            await ctx.send('Resuming')

    @commands.command()
    async def pause(self, ctx):
        voice = get(self.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
            await ctx.send('Pausing')

    @commands.command()
    async def stop(self, ctx):
        voice = get(self.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.stop()
            await ctx.send('Stoping')

    @commands.command()
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount)
        await ctx.send("Clearing")
