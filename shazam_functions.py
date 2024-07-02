from typing import Final
from shazamio import Shazam
import discord

DOWNLOAD_PATH: Final[str] = "bgm/"


async def file_shazam(filePath: str):
    shazam = Shazam()
    data = await shazam.recognize(filePath)

    track = data['track'] if 'track' in data else None

    if track is None:
        return None

    title = track['title']
    artist = track['subtitle']
    img = track['images']['coverart']

    embed = discord.Embed(title=title, colour=discord.Colour.random())
    embed.add_field(name=artist, value='', inline=False)
    embed.set_image(url=img)
    embed.set_footer(text="Powered by ShazamIO")

    return embed







