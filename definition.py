import discord
from typing import List


# PARSE DEFINITION AND CONVERT TO EMBED
def to_list(toJson, definitionCount: int, word: str) -> List[discord.Embed]:
    currentDefinition = ""
    definitionToList = []
    for i in range(definitionCount):
        embed = discord.Embed(title=word, colour=discord.Colour.blue())
        currentDefinition = toJson[i]['meanings'][0]['definitions'][0]['definition']
        embed.add_field(name=currentDefinition, value="", inline=False)
        definitionToList.append(embed)

    return definitionToList
