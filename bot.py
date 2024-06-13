import urllib.request
from typing import Final, Optional
import os
import discord
import openai
import requests
from discord import app_commands
from dotenv import load_dotenv
from openai import OpenAI
import button_paginator as pg
import yandex
import definition
import twitter_embedder
import helper_functions
import apply_filter
import video_tools
import yt_downloader
import twitter_downloader


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
    # YANDEX COMMAND
    @tree.command(name="reverse_search")
    @app_commands.describe(image="Image to reverse")
    async def reverse_search(interaction: discord.Interaction, image: discord.Attachment):
        # check if it's an image
        if not helper_functions.is_image(image):
            await interaction.response.send_message("Provide a valid image file (.png/.jpg)")
            return

        # this command needs to execute within 3 seconds, or it will fail. defer it, so we have more time.
        await interaction.response.defer()
        # read bytes of image
        image_bytes = await image.read()
        result_link = yandex.result_link(image_bytes)
        images = yandex.get_similar_images(result_link)

        # put the image links into a discord embed
        imageToEmbed = yandex.image_embedder(images)

        # put embeds in paginator and send message
        paginator = pg.Paginator(client, imageToEmbed, interaction)
        paginator.default_pagination()
        await paginator.start(deferred=True)

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
            os.remove("img.png")
        else:
            await interaction.response.send_message("Owner only")

    # USE APEX TRACKER TO GET BASIC STATS
    @tree.command(name="apex_stats", description="Gathers basic statistics for an apex user")
    @app_commands.choices(platform=[app_commands.Choice(name="PC", value="PC"),
                                    app_commands.Choice(name="Playstation", value="PS4"),
                                    app_commands.Choice(name="Xbox", value="X1")
                                    ])
    @app_commands.describe(name="Enter username")
    async def apex_stats(interaction: discord.Interaction, platform: app_commands.Choice[str], name: str):
        response = requests.get(
            f"https://api.mozambiquehe.re/bridge?auth={APEXKEY}&player={name}&platform={platform.value}")
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
            embed.add_field(name=f"`Rank:` {basicStats['rank']['rankName']} {basicStats['rank']['rankDiv']}", value="",
                            inline=False)
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
            embed.add_field(name="Remaining Time", value=f"{battleRoyaleData['current']['remainingTimer']}",
                            inline=False)
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
            definitionToList = definition.to_list(toJson, numberOfDefinitions, word)

            # stick the list of embeds in a paginator, which can cycle through definitions easily
            paginator = pg.Paginator(client, definitionToList, interaction)
            paginator.default_pagination()
            await paginator.start()
        else:
            await interaction.response.send_message("Error, try again.")

    # EMBED A TWITTER POST WITH OPTIONAL ARGUMENTS

    # convert all language codes to selectable choices (discord.Choice)
    languageList = twitter_embedder.list_to_choice_list()

    @tree.command(name="twitter_embed", description='Show twitter/X media via fxtwitter with optional args')
    @app_commands.describe(link="Enter link")
    @app_commands.describe(media_only="Media only?")
    @app_commands.choices(translate=languageList)
    async def twitter_embed(interaction: discord.Interaction,
                            link: str,
                            media_only: bool = None,
                            translate: Optional[app_commands.Choice[str]] = None):

        twitterLink: Final[str] = "twitter.com"
        xLink: Final[str] = "x.com"

        if xLink in link:
            link = link.replace(xLink, twitter_embedder.EMBED_LINK)
        elif twitterLink in link:
            link = link.replace(twitterLink, twitter_embedder.EMBED_LINK)
        else:
            await interaction.response.send_message("Link is not a twitter/x link.")
            return

        # if translate checked, add it on
        if translate is not None:
            link += '/' + translate.value

        # if we want the raw media, add it on
        if media_only:
            rawMedia = "d."
            letterToFind = 'f'
            link = link.replace(letterToFind, rawMedia + letterToFind, 1)

        await interaction.response.send_message("[Link](" + link + ")")

    # EMBED TIKTOK VIDEOS
    @tree.command(name="tiktok_embed", description='Embed videos for discord')
    @app_commands.describe(link="Enter link")
    async def tiktok_embed(interaction: discord.Interaction,
                           link: str):

        embedLink: Final[str] = "vxtiktok.com"
        tiktokLink: Final[str] = "tiktok.com"

        if tiktokLink in link:
            link = link.replace(tiktokLink, embedLink)
        else:
            await interaction.response.send_message("Link is not a tiktok.")
            return

        await interaction.response.send_message("[Link](" + link + ")")

    # APPLY A VARIETY OF FACE FILTERS
    @tree.command(name="apply_face_filter", description='Apply filter to a humanoid face')
    @app_commands.choices(choices=[
        app_commands.Choice(name="MLG Shades", value='mlg.png'),
        app_commands.Choice(name="Mustache", value='stache.png'),
        app_commands.Choice(name="Gandalf", value='gandalf.png'),
        app_commands.Choice(name="Robber Mask", value='robber.png'),
        app_commands.Choice(name="Medieval Helmet", value='medieval.png'),
        app_commands.Choice(name="Chill Face", value='chill.png')

    ])
    async def apply_face_filter(interaction: discord.Interaction,
                                image: discord.Attachment,
                                choices: app_commands.Choice[str]):

        if not helper_functions.is_image(image):
            await interaction.response.send_message("Provide a valid image file (.png/.jpg)")
            return

        # START
        folderPath = 'filters/'
        await interaction.response.defer()
        toBytes = await image.read()
        decodedImg = apply_filter.load_image(toBytes)
        result = apply_filter.apply(decodedImg, folderPath + choices.value)

        if not result:
            await interaction.followup.send("Failed to detect faces, upload a better image.")
        else:
            await interaction.followup.send(file=discord.File('filtered_img.png'))
            os.remove("filtered_img.png")

    # SIMPLE VIDEO EDITING
    @tree.command(name="video_tool", description='Do some simple video editing on a supplied video')
    @app_commands.describe(audio="Add a valid audio format to apply to the video chosen (if adding background music)")
    @app_commands.choices(choices=[
        app_commands.Choice(name="Extract audio", value=1),
        app_commands.Choice(name="Add background music", value=2),
        app_commands.Choice(name="Remove audio", value=3)
    ])
    async def video_tool(interaction: discord.Interaction,
                         video: discord.Attachment,
                         choices: app_commands.Choice[int],
                         audio: discord.Attachment = None):

        # make sure its a valid format
        if not helper_functions.is_video(video):
            await interaction.response.send_message("Provide a valid video file (.mp4/.avi/.webm/.mov)")
            return

        # save attachment for processing
        downloadPath = "videos/" + video.filename
        audioDownloadPath = "bgm/" + audio.filename
        outputPath = "videooutput/" + video.filename
        await video.save(downloadPath)

        if choices.value == 2 and audio is not None:
            await audio.save(audioDownloadPath)

        # START
        await interaction.response.defer()
        if choices.value == 1:
            outputPath = video_tools.extract_audio(downloadPath, outputPath)
        elif choices.value == 2:
            video_tools.bgm_add(downloadPath, audioDownloadPath, outputPath)
        elif choices.value == 3:
            video_tools.remove_audio(downloadPath, outputPath)

        await interaction.followup.send(file=discord.File(outputPath))

        os.remove(outputPath)
        os.remove(downloadPath)
        if choices.value == 2:
            os.remove(audioDownloadPath)

    # YOUTUBE DOWNLOADER
    @tree.command(name="youtube", description='Do some youtube conversion (wont work on large durations)')
    @app_commands.describe(link="Youtube URL")
    @app_commands.choices(choices=[
        app_commands.Choice(name="To MP4", value=1),
        app_commands.Choice(name="To MP3", value=2)
    ])
    async def youtube(interaction: discord.Interaction,
                      link: str,
                      choices: app_commands.Choice[int]
                      ):

        # make sure it's a youtube link
        if not link.startswith("https://www.youtube.com") or link.startswith("youtube.com"):
            await interaction.response.send_message("Provide a valid youtube link")
            return

        result = None

        # START
        await interaction.response.defer()
        if choices.value == 1:
            result = yt_downloader.install_mp4(link)
        elif choices.value == 2:
            result = yt_downloader.install_mp3(link)

        if not result:
            await interaction.followup.send("Error, either age restricted or the video is too long")
            return

        if isinstance(result, str):
            print("RETURN TYPE IS STRING")
            await interaction.followup.send(result)
            os.remove(yt_downloader.OUTPUT_PATH + "output.mp4")
        else:
            if choices.value == 1:
                await interaction.followup.send(file=discord.File(yt_downloader.OUTPUT_PATH + "output.mp4"))
                os.remove(yt_downloader.OUTPUT_PATH + "output.mp4")
            else:
                await interaction.followup.send(file=discord.File(yt_downloader.OUTPUT_PATH + "output.mp3"))
                os.remove(yt_downloader.OUTPUT_PATH + "output.mp3")

    @tree.command(name="twitter_download", description='Download twitter/X videos')
    @app_commands.describe(link="Enter link")
    async def twitter_download(interaction: discord.Interaction,
                               link: str):

        xLink: Final[str] = "https://twitter.com"
        twitterLink: Final[str] = "https://x.com"

        await interaction.response.defer()
        if link.startswith(xLink) or link.startswith(twitterLink):
            result = twitter_downloader.download(link)
        else:
            await interaction.response.send_message("Link is not twitter")
            return

        if not result:
            await interaction.followup.send("Twitter link has no video")
            return

        await interaction.followup.send(file=discord.File(twitter_downloader.DOWNLOAD_PATH))
        os.remove(twitter_downloader.DOWNLOAD_PATH)

    client.run(token=TOKEN)
