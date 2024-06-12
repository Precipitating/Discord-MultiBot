import pytube.exceptions
import responses
from pytubefix import YouTube
from typing import Final
import requests

DISCORD_MAX_FILE_SIZE_MB: Final[int] = 25
LITTERBOX_UPLOAD_LIMIT: Final[int] = 1000
OUTPUT_PATH: Final[str] = "videooutput/"
HOST_API: Final[str] = "https://litterbox.catbox.moe/resources/internals/api.php"


# return types:
# NONE = failed to download or host video - ERROR
# True = downloaded video, under 25mb and can send video directly to discord - DOWNLOAD -> SEND
# string = url of a hosted video over 25mb - DOWNLOAD -> HOST
def install_mp4(link: str):
    toYT = YouTube(link)

    # get video
    try:
        vid = toYT.streams.get_highest_resolution()
        vid.download(filename="output.mp4", output_path=OUTPUT_PATH)
        print("mp4 downloaded")
    except pytube.exceptions.AgeRestrictedError:
        print("age restricted video")
        return None

    # try hosting on a site if over 25mb
    fileSize = toYT.streams.get_highest_resolution().filesize_mb
    # if over 25mb and under 1gb, we can host this
    if DISCORD_MAX_FILE_SIZE_MB < fileSize < LITTERBOX_UPLOAD_LIMIT:
        print("Over 25mb, trying alternative method:")
        with open(OUTPUT_PATH + "output.mp4", 'rb') as file:
            files = {
                'reqtype': (None, 'fileupload'),
                'time': (None, '1h'),
                'fileToUpload': file
            }
            # will take a while to upload the video depending on how big it is
            response = requests.post(HOST_API, files=files)

            if response.status_code == 200:
                # url to the hosted video
                return response.text
            else:
                print("api failed to upload")
                return None

    # if we're here, then no need to host, send file directly
    return True


def install_mp3(link: str):
    toYT = YouTube(link)
    vid = toYT.streams.get_audio_only()
    vid.download(output_path=OUTPUT_PATH, filename="output", mp3=True)
    return True
