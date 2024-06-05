import urllib.request
from typing import Final, List
import os
import discord
import openai
import requests
from discord import app_commands, embeds
from dotenv import load_dotenv
from openai import OpenAI
import button_paginator as pg
import json
from bs4 import BeautifulSoup


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

    # REVERSE AN IMAGE VIA YANDEX AND RETURN SIMILAR IMAGES

    # get yandex link
    def yandex_result_link(image_bytes: bytes) -> str:
        search_url = 'https://yandex.ru/images/search'
        files = {'upfile': ('blob', image_bytes, 'image/jpeg')}
        params = {'rpt': 'imageview', 'format': 'json',
                  'request': '{"blocks":[{"block":"b-page_type_search-by-image__link"}]}'}
        response = requests.post(search_url, params=params, files=files)
        query_string = json.loads(response.content)['blocks'][0]['params']['url']
        img_search_url = search_url + '?' + query_string
        print(img_search_url)
        return img_search_url

    # scrape the "site" section to get similar images
    def get_similar_images(targetLink: str) -> List[str]:
        page = requests.get(targetLink)
        soup = BeautifulSoup(page.text, "html.parser")
        similar_image_section = soup.find_all("img", class_="MMImage Thumb-Image")
        img: list[str] = []

        for icon in similar_image_section:
            imgLink = icon.get('src')
            if not imgLink.startswith("https://"):
                img.append("https:" + imgLink)
            else:
                img.append(imgLink)
            print(img[-1])
        return img

    @tree.command(name="reverse_search")
    @app_commands.describe(image="Image to reverse")
    async def reverse_search(interaction: discord.Interaction, image: discord.Attachment):
        # this command needs to execute within 3 seconds, or it will fail. defer it, so we have more time.
        await interaction.response.defer()
        image_bytes = await image.read()
        result_link = yandex_result_link(image_bytes)
        images = get_similar_images(result_link)


        # embed the image links
        imageToEmbed = []
        for image in images:
            embed = discord.Embed(title="Image", description="", colour=discord.Colour.random())
            embed.set_image(url=image)
            imageToEmbed.append(embed)


        # put embeds in paginator
        paginator = pg.Paginator(client, imageToEmbed, interaction)
        paginator.default_pagination()
        await paginator.start(deferred=True)
        print("success")

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
        else:
            await interaction.response.send_message("Owner only")


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

            embed = discord.Embed(title="Player Statistics", description="", colour=discord.Colour.random())
            # Name
            embed.add_field(name=f"`Name:` {name}  ", value="", inline=False)
            # Level
            embed.add_field(name=f"`Level:` {basicStats['level']} ", value="", inline=False)
            # Bans
            embed.add_field(name=f"`Banned:` {basicStats['bans']['isActive']}", value="", inline=False)
            embed.add_field(name=f"`Last Ban Reason:` {basicStats['bans']['last_banReason']}", value="", inline=False)
            # Rank
            embed.add_field(name=f"`Rank:` {basicStats['rank']['rankName']} {basicStats['rank']['rankDiv']}", value="", inline=False)
            # Status
            embed.add_field(name=f"`Status:` {realtimeStats['currentState']}", value="", inline=False)

            await interaction.response.send_message(embed=embed)

        else:
            await interaction.response.send_message("Data failed to collect."
                                                    "Ensure correct information is submitted & try again")

    # GET APEX MAP ROTATION DATA
    @tree.command(name="apex_map_rotation", description="Gathers apex map rotation")
    async def apex_map_rotation(interaction: discord.Interaction):
        response = requests.get(
            f"https://api.mozambiquehe.re/maprotation?auth={APEXKEY}", params={'version': 2})
        if response.status_code == 200:
            toJson = response.json()
            battleRoyaleData = toJson['battle_royale']
            rankedData = toJson['ranked']

            embed = discord.Embed(title="Apex Legends Map Rotation", description="", colour=discord.Colour.random())
            # Battle Royale
            embed.add_field(name="BATTLE ROYALE:", value="", inline=False)
            embed.add_field(name="Current Map: ", value=f"{battleRoyaleData['current']['map']}")
            embed.add_field(name="Next Map: ", value=f"{battleRoyaleData['next']['map']}", inline=True)
            embed.add_field(name="Remaining Time", value=f"{battleRoyaleData['current']['remainingTimer']}", inline=False)
            # Ranked
            embed.add_field(name="RANKED:", value="", inline=False)
            embed.add_field(name="Current Map:", value=f"{rankedData['current']['map']}")
            embed.add_field(name="Next Map: ", value=f"{rankedData['next']['map']}", inline=True)
            embed.add_field(name="Remaining Timer:", value=f"{rankedData['current']['remainingTimer']}", inline=False)

            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("Map rotation failed to collect."
                                                    "Try again in 5s.")


    # SYNC DATA
    @tree.command(name="sync", description='Owner only')
    async def sync(interaction: discord.Interaction):
        if interaction.user.id == OWNER:
            await tree.sync()
            await interaction.response.send_message("Synced")
        else:
            await interaction.response.send_message("Only the owner can use this command.")

    # parse the definition and put it in a discord embed
    def definition_to_list(toJson, definitionCount, word):
        currentDefinition = ""
        definitionToList = []
        for i in range(definitionCount):
            embed = discord.Embed(title=word, colour=discord.Colour.blue())
            currentDefinition = toJson[i]['meanings'][0]['definitions'][0]['definition']
            embed.add_field(name=currentDefinition, value="", inline=False)
            definitionToList.append(embed)

        return definitionToList

    # DEFINE A WORD
    @tree.command(name="define", description='Get the definition of any word')
    @app_commands.describe(word="Enter the word you want to know about")
    async def define(interaction: discord.Interaction, word: str):
        response = requests.get(
            f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        if response.status_code == 200:
            toJson = response.json()
            # add all the definitions into a list of embeds
            numberOfDefinitions = len(toJson)
            definitionToList = definition_to_list(toJson, numberOfDefinitions, word)

            # stick the list of embeds in a paginator, which can cycle through definitions easily
            paginator = pg.Paginator(client, definitionToList, interaction)
            paginator.default_pagination()
            await paginator.start()

        else:
            await interaction.response.send_message("Error, try again.")

    client.run(token=TOKEN)
