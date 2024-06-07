import requests
from bs4 import BeautifulSoup
import json
import discord
from typing import List

# GET YANDEX LINK
def result_link(image_bytes: bytes) -> str:
    search_url = 'https://yandex.ru/images/search'
    files = {'upfile': ('blob', image_bytes, 'image/jpeg')}
    params = {'rpt': 'imageview', 'format': 'json',
              'request': '{"blocks":[{"block":"b-page_type_search-by-image__link"}]}'}
    response = requests.post(search_url, params=params, files=files)
    query_string = json.loads(response.content)['blocks'][0]['params']['url']
    img_search_url = search_url + '?' + query_string
    print(img_search_url)
    return img_search_url


# SCRAPE THE LINK AND GET SIMILAR IMAGES
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


# embed the image links
def image_embedder(images: List[str]) -> List[discord.Embed]:
    imageToEmbed = []
    for image in images:
        embed = discord.Embed(title="Image", description="", colour=discord.Colour.random())
        embed.set_image(url=image)
        imageToEmbed.append(embed)
    return imageToEmbed