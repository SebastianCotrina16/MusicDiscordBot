import asyncio
import os
import discord
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from discord import TextChannel
import yt_dlp as youtube_dl

intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix=".", intents=intents)
players = {}

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'quiet': True,
}
@client.event
async def on_ready():
    print('Bot online')
@client.command()
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

async def disconnect_after_inactivity(voice_client):
    await asyncio.sleep(120)
    if not voice_client.is_playing() and not voice_client.is_paused():
        await voice_client.disconnect()

@client.command()
async def play(ctx, *, url):
    channel = ctx.author.voice.channel

    voice_client = ctx.guild.voice_client

    if voice_client is None or not voice_client.is_connected():
        voice_client = await channel.connect()

    if voice_client.is_playing():
        voice_client.stop()
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

        if "formats" not in info:
            return await ctx.send("No se pudo obtener la información del formato del video.")

        best_audio = max(info["formats"], key=lambda f: f.get("abr", 0))
        audio_url = best_audio["url"]

    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
    }
    voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=audio_url, **FFMPEG_OPTIONS))

    # Programar la desconexión después de 2 minutos de inactividad
    asyncio.create_task(disconnect_after_inactivity(voice_client))

@client.command()
async def resume(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        voice.resume()
        await ctx.send('Resumiendo')


@client.command()
async def pause(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.pause()
        await ctx.send('Stop')


@client.command()
async def stop(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.stop()
        await ctx.send('Parando...')


@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)
    await ctx.send("Clear")

client.run("MTAyNzk3NDUxMzQxOTM1ODMyOQ.Gtivdr._DccNS-TcFQbPU51UsaA4eqZnaZMx97lk13fik")


