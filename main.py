import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import os
import asyncio
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, AudioConfig, ResultReason

client = commands.Bot(command_prefix = '`',intents=discord.Intents.all())

azure_key = "420cdbf55b834a7ebe07ad1444242e2c"
azure_region = "australiaeast"
speech_config = SpeechConfig(subscription=azure_key, region=azure_region)
audio_config = AudioConfig(filename="output.wav")
synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
@client.event
async def join(ctx):
        voice_channel = ctx.author.voice.channel
        if voice_channel:
            voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
            if voice_client:
                await ctx.channel.send("The bot is already in a voice channel")
            else:
                voice_client = await voice_channel.connect()
        else:
            await ctx.channel.send("You need to be in a voicechat to use the bot")






@client.event
async def on_message(message):
    if message.content.startswith("!"):
        if message.channel.name == "fort" and message.author != client.user and message.content.startswith != "`join" and message.content.startswith != "`leave":
            result = synthesizer.speak_text_async(message.content).get()
            if result.reason == ResultReason.SynthesizingAudioCompleted:
                voice_channel = message.author.voice.channel
                if voice_channel:
                    voice_client = discord.utils.get(client.voice_clients, guild=message.guild)
                    if voice_client:
                        await play_audio(voice_client)
                    else:
                        voice_client = await voice_channel.connect()
                        await play_audio(voice_client)
                else:   
                    await message.channel.send("You need to be in a voice channel for me to join.")

async def play_audio(voice_client):
    voice_client.play(discord.FFmpegPCMAudio("output.wav"))

@client.command
async def leave(ctx):
    voice = ctx.author.channel
    if ctx.voice:
        await ctx.guild.voice.disconnect()
        await ctx.send("Left the voice channel.")

client.run("MTIzNDQ1Mjk5MDUwMTQ1Mzg4Ng.GqDMnu.5aREcly7m40VQDa1QZlkFXfRG2tU5GkL3HA_K8")