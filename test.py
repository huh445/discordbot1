import discord
from discord import FFmpegPCMAudio
import yt_dlp
from discord.ext import commands

# Intents with message content for handling slash command content
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=".", intents=intents)

@bot.command()
async def join(ctx):
    voice_channel = ctx.author.voice.channel
    if voice_channel:
        voice_bot = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice_bot:
            await ctx.send("The bot is already in a voice channel")
        else:
            voice_bot = await voice_channel.connect()
            await ctx.send("Joined the voice channel")
    else:
        await ctx.send("You need to be in a voicechat to use the bot")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def play(ctx, url):
    voice_channel = ctx.author.voice.channel
    if voice_channel:
        vc = await voice_channel.connect()
        try:
            with yt_dlp.YoutubeDL({'format': 'bestaudio'}) as ydl:
                info = ydl.extract_info(url, download=False)
                url2 = info['formats'][0]['url']
                vc.play(discord.FFmpegPCMAudio(url2, executable="C:/Users/charc/Downloads/ffmpeg-master-latest-win64-gpl/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe"), after=lambda e: print('done', e))
        except Exception as e:
            print(f"An error occurred while playing audio: {e}")
            await ctx.send("An error occurred while playing audio.")
            await vc.disconnect()
    else:
        await ctx.send("You need to be in a voice channel to use this command.")



@bot.command()
async def leave(ctx):
    voice_bot = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_bot:
        await voice_bot.disconnect()
    else:
        await ctx.send("Left the voice channel")

@bot.command()
async def stop(ctx):
    voice_client = ctx.voice_client
    if voice_client:
        await voice_client.disconnect()
    else:
        await ctx.send("Not connected to a voice channel")

bot.run("MTA0MTE2NTYxMDQ2NzQ3OTU1Mg.G3NP7u.02-reMkhAcGTjGUxB7njR_ZAwDSQ9gSEbYeTS4")  # Replace with your actual bot token

#bot token for future refernce MTIzNDQ1Mjk5MDUwMTQ1Mzg4Ng.GMQSwb.BqGLkG6KsRXmx6IIlmGDNiZsfL2Z2_tV7Ymi34
#other token MTA0MTE2NTYxMDQ2NzQ3OTU1Mg.G3NP7u.02-reMkhAcGTjGUxB7njR_ZAwDSQ9gSEbYeTS4