import discord
import numpy as np
from io import BytesIO
import os
import glob
import cv2
import matplotlib.pyplot as plt
import insightface
from insightface.app import FaceAnalysis
from insightface.data import get_image as ins_get_image
from typing import Final
from PIL import Image

import apply_filter

FACE_SWAP_SAVE_PATH: Final[str] = 'img/output.png'
FACE_SWAP_SAVE_PATH2: Final[str] = 'img/output2.png'


# detect faces, if none, then return a Discord error.
async def swap_face(interaction: discord.Interaction, img1: bytes, img2: bytes, choices: int):
    app = FaceAnalysis(name='buffalo_l')
    swapper = insightface.model_zoo.get_model('models/inswapper_128.onnx', download=False, download_zip=False)
    app.prepare(ctx_id=0, det_size=(640, 640))
    # convert bytes to readable format for matplot
    decodedImg1 = np.array(apply_filter.load_image(img1))
    decodedImg2 = np.array(apply_filter.load_image(img2))

    # detect faces
    sourceFace = app.get(decodedImg1)
    destinationFaces = app.get(decodedImg2)

    if choices == 1:
        if len(sourceFace) == 0 or len(destinationFaces) == 0:
            await interaction.followup.send("Either both images have no faces detected, or one face is not detected "
                                            "in an img")
            return -1
        sourceFace = sourceFace[0]
        for face in destinationFaces:
            decodedImg2 = swapper.get(decodedImg2, face, sourceFace, paste_back=True)

        cv2.imwrite(FACE_SWAP_SAVE_PATH, decodedImg2)

    elif choices == 2:
        if len(sourceFace) > 1 and len(destinationFaces) > 1:
            await interaction.followup.send("Make sure both images have one face")
            return -1
        if len(sourceFace) == 0 or len(destinationFaces) == 0:
            await interaction.followup.send("Either both images have no faces detected, or one face is not detected "
                                            "in an img")
            return -1

        # swap both faces and save
        sourceFace = sourceFace[0]
        destinationFaces = destinationFaces[0]
        decodedImg1 = swapper.get(decodedImg1, sourceFace, destinationFaces, paste_back=True)
        decodedImg2 = swapper.get(decodedImg2, destinationFaces, sourceFace, paste_back=True)
        cv2.imwrite(FACE_SWAP_SAVE_PATH, decodedImg1)
        cv2.imwrite(FACE_SWAP_SAVE_PATH2, decodedImg2)










