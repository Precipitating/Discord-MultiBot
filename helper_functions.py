import discord


def is_image(file: discord.Attachment):
    # check if it's an image
    if file.filename.endswith(('.png', '.jpg', '.jpeg')):
        return True
    else:
        return False
