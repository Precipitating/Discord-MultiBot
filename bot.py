import urllib.request
from typing import Final
import os
import discord
import openai
import requests
from discord import app_commands
from dotenv import load_dotenv
from openai import OpenAI


def run_bot():
    # SET TOKEN
    load_dotenv()
    TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
    OWNER: Final[int] = int(os.getenv('OWNER_ID'))
    OPENAIKEY: Final[str] = os.getenv('OPENAI_API_KEY')
    APEXKEY: Final[str] = os.getenv('APEX_API_KEY')

    # SET BOT
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    tree = app_commands.CommandTree(client)
    openAIClient = OpenAI()
    openai.api_key = OPENAIKEY

    @client.event
    async def on_ready():
        print("Multibot running")

    # REVERSE AN IMAGE VIA YANDEX AND RETURN RESULTS
    @tree.command(name="reverse_search")
    @app_commands.describe(image="Image to reverse")
    async def reverse_search(interaction: discord.Interaction, image: discord.Attachment):
        await interaction.response.send_message("Reverse search running...")

    # USE OPENAI TO GENERATE AN IMAGE
    @tree.command(name="generate_image", description="Owner only")
    @app_commands.describe(text="Describe the image you want")
    async def generate_image(interaction: discord.Interaction, text: str):
        if interaction.user.id == OWNER:
            await interaction.response.send_message("Generating image...")
            response = openAIClient.images.generate(
                model="dall-e-3",
                prompt=text,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            image_url = response.data[0].url
            urllib.request.urlretrieve(image_url, "img.png")
            await interaction.channel.send(content=f"Image for {text}", file=discord.File("img.png"))

    # USE APEX TRACKER TO GET BASIC STATS
    @tree.command(name="apex_stats", description="Gathers basic statistics for an apex user")
    @app_commands.describe(platform="Enter platform (PC,PS4,X1)")
    @app_commands.describe(name="Enter username")
    async def apex_stats(interaction: discord.Interaction, platform: str, name: str):
        response = requests.get(
            f"https://api.mozambiquehe.re/bridge?auth={APEXKEY}&player={name}&platform={platform}")
        if response.status_code == 200:
            toJson = response.json()
            basicStats = toJson['global']
            realtimeStats = toJson['realtime']
            await interaction.response.send_message(f"Name: {name} \n"
                                                    f"Level: {basicStats['level']} \n"
                                                    f"Banned?: {basicStats['bans']['isActive']} \n"
                                                    f"Rank: {basicStats['rank']['rankName']} {basicStats['rank']['rankDiv']} \n"
                                                    f"Status: {realtimeStats['currentState']} \n"
                                                    )

        else:
            await interaction.response.send_message("Data failed to collect."
                                                    "Ensure correct information is submitted & try again")

    @tree.command(name="sync", description='Owner only')
    async def sync(interaction: discord.Interaction):
        if interaction.user.id == OWNER:
            await tree.sync()
            await interaction.response.send_message("Synced")
        else:
            await interaction.response.send_message("Only the owner can use this command.")

    client.run(token=TOKEN)
