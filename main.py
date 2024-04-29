import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import os
import asyncio
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, AudioConfig, ResultReason

source = FFmpegPCMAudio("huh445-hebuiltgary.mp3")

client = commands.Bot(command_prefix = '!',intents=discord.Intents.all())

azure_key = "420cdbf55b834a7ebe07ad1444242e2c"
azure_region = "australiaeast"
speech_config = SpeechConfig(subscription=azure_key, region=azure_region)
audio_config = AudioConfig(filename="output.wav")
synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

@client.event
async def on_message(message):
    if message.channel.name == "fort" and message.author != client.user:
        # Convert text to speech
        result = synthesizer.speak_text_async(message.content).get()
        if result.reason == ResultReason.SynthesizingAudioCompleted:
            # Get the voice channel of the user who sent the message
            voice_channel = message.author.voice.channel
            if voice_channel:
                # Check if the bot is already in a voice channel
                voice_client = discord.utils.get(client.voice_clients, guild=message.guild)
                if voice_client:
                    # If the bot is already in a voice channel, use the existing voice client
                    await play_audio(voice_client)
                else:
                    # If the bot is not in a voice channel, connect to the user's voice channel
                    voice_client = await voice_channel.connect()
                    await play_audio(voice_client)
            else:
                await message.channel.send("You need to be in a voice channel for me to join.")

async def play_audio(voice_client):
    # Play the synthesized speech
    voice_client.play(discord.FFmpegPCMAudio("output.wav"))
    # Wait for the audio to finish playing
    while voice_client.is_playing():
        await asyncio.sleep(1)
    # Disconnect from the voice channel after playing
    await voice_client.disconnect()

client.run("MTIzNDQ1Mjk5MDUwMTQ1Mzg4Ng.GqDMnu.5aREcly7m40VQDa1QZlkFXfRG2tU5GkL3HA_K8")