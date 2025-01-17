import discord
from discord import FFmpegOpusAudio
import asyncio
from discord import app_commands
from discord.ext import commands
import yt_dlp

# Intents with message content for handling slash command content
intents = discord.Intents.default()
intents.message_content = True

# Create the bot instance
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)
client = commands.Bot(command_prefix=".", intents=intents)

@tree.command(
    name="join",
    description="Joined the voice call"
)
async def join(interaction):
    voice_channel = interaction.user.voice.channel
    if voice_channel:
        voice_bot = discord.utils.get(bot.voice_clients, guild=interaction.guild)  # Use voice_clients instead of voice_bots
        if voice_bot:
            await interaction.response.send_message("The bot is already in a voice channel")
        else:
            voice_bot = await voice_channel.connect()
            await interaction.response.send_message("Joined the voice channel")
    else:
        await interaction.response.send_message("You need to be in a voicechat to use the bot")


@bot.event
async def on_ready():
    await tree.sync()  # Register slash commands globally
    print(f"Logged in as {bot.user}")

async def play_audio(voice_bot):
    try:  # Add error handling for potential exceptions
        voice_bot.play(discord.FFmpegOpusAudio("output.wav"))
        return
    except Exception as e:
        print(f"Error playing audio: {e}")


@tree.command(
    name="leave",
    description="Leave the current voice call"
)
async def leave(interaction):
    voice_bot = discord.utils.get(bot.voice_clients, guild=interaction.guild)
    if voice_bot:
        await voice_bot.disconnect()
        await interaction.response.send_message("Left the voice channel")
    else:
        await interaction.response.send_message("Not in a voice channel")

@tree.command(
        name="yt",
        description="Plays a youtube video"
)
async def yt(interaction, url: str):
    voice_channel = interaction.user.voice.channel
    if voice_channel:
        vc = discord.utils.get(bot.voice_clients, guild=interaction.guild)
        await interaction.response.defer(ephemeral=True)
        if vc:
            print("yarp they in a vc fr fr on god")
        else:
            vc = await voice_channel.connect()
        try:
            with yt_dlp.YoutubeDL({"format": "bestaudio/best", "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "opus", "preferredquality": "192"}]}) as ydl:
                info = ydl.extract_info(url, download=False)

                audio_url = info["url"]
                audio_duration = info["duration"]
                audio_title = info["title"]

                await interaction.followup.send(f"Now playing: {audio_title} (approx. {int(audio_duration // 60)}m {audio_duration % 60}s)")
                if vc.is_connected():
                    player = vc.play(FFmpegOpusAudio(audio_url))
        except yt_dlp.utils.DownloadError as e:
            await interaction.followup.send(f"An error occurred while processing audio: {str(e)}")
        except Exception as e:
            await interaction.followup.send(f"An unexpected error occured: {str(e)}")
    else:
        await interaction.followup.send("You need to be in a voice channel to use this command.")



bot.run("")  # Replace with your actual bot token