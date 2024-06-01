import urllib.request
from typing import Final
import os
import discord
import openai
from discord import app_commands
from dotenv import load_dotenv
from openai import OpenAI


def run_bot():
    # SET TOKEN
    load_dotenv()
    TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
    OWNER: Final[str] = os.getenv('OWNER_ID')
    OPENAIKEY: Final[str] = os.getenv('OPENAI_API_KEY')

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
    @tree.command(name="generate_image")
    @app_commands.describe(text="Describe the image you want")
    async def generate_image(interaction: discord.Interaction, text: str):
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

        # USE APEX TRACKER TO GET INFO
        @tree.command(name="apex_stats")
        @app_commands.describe(text="Enter origin username")
        async def generate_image(interaction: discord.Interaction, text: str):
            await interaction.response.send_message("Gathering Info...")

    @tree.command(name="sync", description= 'Owner only')
    async def sync(interaction: discord.Interaction):
        if interaction.user.id == OWNER:
            await tree.sync()
            print('Command tree synced')
        else:
            await interaction.response.send_message("Only the owner can use this command.")

    client.run(token=TOKEN)

