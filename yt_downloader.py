import asyncio
import aiohttp
import pytube.exceptions
from pytubefix import YouTube
from typing import Final

DISCORD_MAX_FILE_SIZE_MB: Final[int] = 25
LITTERBOX_UPLOAD_LIMIT: Final[int] = 1000
OUTPUT_PATH: Final[str] = "videooutput/"
OUTPUT_NAME: Final[str] = "output"
HOST_API: Final[str] = "https://litterbox.catbox.moe/resources/internals/api.php"
TIMEOUT_DURATION: Final[int] = 180 # in seconds


# return types:
# NONE = failed to download or host video - ERROR
# True = downloaded video, under 25mb and can send video directly to discord - DOWNLOAD -> SEND
# string = url of a hosted video over 25mb - DOWNLOAD -> HOST
async def install_mp4(link: str):
    toYT = YouTube(link)

    # get video
    try:
        vid = toYT.streams.get_highest_resolution()
        vid.download(filename=OUTPUT_NAME+'.mp4', output_path=OUTPUT_PATH)
        print("mp4 downloaded")

    except pytube.exceptions.AgeRestrictedError:
        print("age restricted video")
        return None

    # try hosting on a site if over 25mb
    fileSize = toYT.streams.get_highest_resolution().filesize_mb
    # if over 25mb and under 1gb, we can host this
    if DISCORD_MAX_FILE_SIZE_MB < fileSize < LITTERBOX_UPLOAD_LIMIT:
        print("Over 25mb, trying alternative method:")
        with open(OUTPUT_PATH + OUTPUT_NAME+'.mp4', 'rb') as file:
            # will take a while to upload the video depending on how big it is
            # use asyncio, so it doesn't block discord's heartbeat
            data = aiohttp.FormData()
            data.add_field('reqtype', 'fileupload')
            data.add_field('time', '1h')
            data.add_field('fileToUpload', file, filename='output.mp4',
                           content_type='video/mp4')
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(url=HOST_API, data=data, timeout=TIMEOUT_DURATION) as r:
                        if r.status == 200:
                            return await r.text()
                        else:
                            print("api failed to upload to litterbox")
                            return None
            except asyncio.TimeoutError:
                print("took too long to upload to server")
                return None


    # if we're here, then no need to host, send file directly
    print("no need to host, send locally")
    return True


def install_mp3(link: str, outputPath: str):
    toYT = YouTube(link)
    vid = toYT.streams.get_audio_only()
    vid.download(output_path=outputPath, filename=f"{OUTPUT_NAME}", mp3=True)
    return True
