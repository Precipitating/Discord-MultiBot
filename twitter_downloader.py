import bs4
import discord.app_commands.errors
import requests
from typing import Final

DOWNLOADER_URL: Final[str] = "https://twitsave.com/info?url="
CHUNK_SIZE: Final[int] = 1024
DOWNLOAD_PATH: Final[str] = "videooutput/output.mp4"


# use website twitsave to get the raw mp4 and download the url itself
def download(link: str):
    fullLink = DOWNLOADER_URL + link
    # fetch page
    response = requests.get(fullLink)
    data = bs4.BeautifulSoup(response.text, 'html.parser')

    # get download link of highest quality video
    try:
        highestQualityElem = data.find_all('div', class_="origin-top-right")[0].find_all('a')[0].get('href')
    except:
        return False

    # download the url to videooutput folder
    downloadResponse = requests.get(highestQualityElem, stream=True)
    if downloadResponse.status_code == 200:
        with open(DOWNLOAD_PATH, 'wb') as file:
            for data in downloadResponse.iter_content(chunk_size=CHUNK_SIZE):
                file.write(data)

    print("DOWNLOADED FILE")
    return True
