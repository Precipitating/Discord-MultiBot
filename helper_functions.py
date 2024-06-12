import discord
import os


def is_image(file: discord.Attachment):
    # check if it's an image
    if file.filename.endswith(('.png', '.jpg', '.jpeg')):
        return True
    else:
        return False


def is_video(file: discord.Attachment):
    # check if it's an image
    if file.filename.endswith(('.mp4', '.webm', '.avi', '.mov')):
        return True
    else:
        return False


def is_audio(file: discord.Attachment):
    # check if it's an image
    if file.filename.endswith(('.mp3', '.wav', '.ogg', '.wma', '.m4a', '.aac')):
        return True
    else:
        return False



def extract_file_format(file: str):
    _, fileExtension = os.path.splitext(file)

    return fileExtension
