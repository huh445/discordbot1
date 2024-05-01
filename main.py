import discord
from discord import FFmpegPCMAudio
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, AudioConfig, ResultReason
import asyncio
from discord import app_commands

# Intents with message content for handling slash command content
intents = discord.Intents.default()
intents.message_content = True

# Create the bot instance
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

azure_key = "420cdbf55b834a7ebe07ad1444242e2c"  # Replace with your actual key
azure_region = "australiaeast"
audio_config = AudioConfig(filename="output.wav")

@tree.command(
    name="join",
    description="Join the voice call"
)
async def join(interaction):
    voice_channel = interaction.author.voice.channel
    if voice_channel:
        voice_bot = discord.utils.get(bot.voice_clients, guild=interaction.guild)  # Use voice_clients instead of voice_bots
        if voice_bot:
            await interaction.channel.send("The bot is already in a voice channel")
        else:
            voice_bot = await voice_channel.connect()
            await interaction.channel.send("Joined the voice channel")
    else:
        await interaction.channel.send("You need to be in a voicechat to use the bot")


@bot.event
async def on_ready():
    await tree.sync()  # Register slash commands globally
    print(f"Logged in as {bot.user}")
async def play_audio(voice_bot):
    try:  # Add error handling for potential exceptions
        voice_bot.play(discord.FFmpegPCMAudio("output.wav"))
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
        await interaction.send("Left the voice channel.")
    else:
        await interaction.respond("Not in a voice channel")


#Uncomment and modify this section if you want to re-enable text-to-speech functionality
@tree.command(
    name="tts",
    description="Converts text to speech and plays it in your voice channel"
)
async def tts(interaction, text: str):
    """
    This command takes text as input, synthesizes it into speech, and plays it
    in the user's voice channel. Accepts multi-word sentences.

    Args:
        text (str): The text to be converted to speech (passed as an option).
    """
    try:
        # Create a new SpeechSynthesizer instance for each command
        speech_config = SpeechConfig(subscription=azure_key, region=azure_region)
        synthesizer = SpeechSynthesizer(speech_config=speech_config)

        result = synthesizer.speak_text_async(text).get()
        if result.reason == ResultReason.SynthesizingAudioCompleted:
            voice_channel = interaction.author.voice.channel
            if voice_channel:
                voice_bot = discord.utils.get(bot.voice_clients, guild=interaction.guild)
                if not voice_bot or not voice_bot.is_connected():
                    voice_bot = await voice_channel.connect()
                await play_audio(voice_bot)
            else:
                await interaction.respond("You need to be in a voicechat to use the bot")
    except Exception as e:
        print(f"Error synthesizing speech: {e}")
        await interaction.respond("Error synthesizing speech. Please try again later.")
    finally:
        # Handle potential missing close method using hasattr
        if hasattr(synthesizer, 'close'):
            synthesizer.close()  # Close synthesizer if available

bot.run("MTIzNDQ1Mjk5MDUwMTQ1Mzg4Ng.GMQSwb.BqGLkG6KsRXmx6IIlmGDNiZsfL2Z2_tV7Ymi34")  # Replace with your actual bot token

#bot token for future refernce MTIzNDQ1Mjk5MDUwMTQ1Mzg4Ng.GMQSwb.BqGLkG6KsRXmx6IIlmGDNiZsfL2Z2_tV7Ymi34