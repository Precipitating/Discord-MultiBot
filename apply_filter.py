import cv2
import cvzone
import numpy as np
import math
from typing import Union, Final

STACHE_Y_SIZE_MULTIPLIER: Final[float] = 0.5
STACHE_X_MULTIPLIER: Final[float] = -0.75
STACHE_Y_MULTIPLIER: Final[float] = -0.25

GANDALF_X_SIZE_MULTIPLIER: Final[float] = 2.5
GANDALF_Y_SIZE_MULTIPLIER: Final[float] = 2.5
GANDALF_X_MULTIPLIER: Final[float] = -0.22
GANDALF_Y_MULTIPLIER: Final[float] = -0.16

ROBBER_X_SIZE_MULTIPLIER: Final[float] = 1.1
ROBBER_Y_SIZE_MULTIPLIER: Final[float] = 1.5
ROBBER_X_MULTIPLIER: Final[float] = -0.02
ROBBER_Y_MULTIPLIER: Final[float] = -0.22

MEDIEVAL_X_SIZE_MULTIPLIER: Final[float] = 2
MEDIEVAL_Y_SIZE_MULTIPLIER: Final[float] = 1.5
MEDIEVAL_X_MULTIPLIER: Final[float] = -0.23
MEDIEVAL_Y_MULTIPLIER: Final[float] = -0.27

CHILL_X_SIZE_MULTIPLIER: Final[float] = 0.85
CHILL_Y_SIZE_MULTIPLIER: Final[float] = 0.2
CHILL_X_MULTIPLIER: Final[float] = -0.6
CHILL_Y_MULTIPLIER: Final[float] = -0.1

CHILL_X_SIZE_MULTIPLIER_MOUTH: Final[float] = 0.85
CHILL_Y_SIZE_MULTIPLIER_MOUTH: Final[float] = 0.2
CHILL_X_MULTIPLIER_MOUTH: Final[float] = -1.6
CHILL_Y_MULTIPLIER_MOUTH: Final[float] = 0.1





def load_image(img: bytes) -> Union[np.ndarray, None]:
    # decode to a readable format for OpenCV
    imageArray = np.frombuffer(img, np.uint8)
    decodedImage = cv2.imdecode(imageArray, cv2.IMREAD_COLOR)

    if decodedImage is None:
        print("Discord Attachment image cannot be decoded")
        return

    return decodedImage


# resize the image overlay to a suitable size and position it correctly
def resize_and_position_landmark(overlay, img, box, landmarks, xSizeMultiplier=1.0, ySizeMultiplier=1.0,
                                 xMultiplier=0.0,
                                 yMultiplier=0.0):
    overlayResize = cv2.resize(overlay, (int(box[2] * xSizeMultiplier), int(box[3] * ySizeMultiplier)))
    # since origin is top left of image, we need to apply an offset, so it is positioned correctly.
    # (nose landmark) - (overlay x/y size) * (multiplier calculated manually).
    img = cvzone.overlayPNG(img, overlayResize, [int(landmarks[0] + (overlayResize.shape[0] * xMultiplier)),
                                                 int(landmarks[1] + (overlayResize.shape[1] * yMultiplier))])


def resize_and_position_default(overlay, img, box, xSizeMultiplier=1.0, ySizeMultiplier=1.0,
                                xMultiplier=0.0,
                                yMultiplier=0.0):
    overlayResize = cv2.resize(overlay, (int(box[2] * xSizeMultiplier), int(box[3] * ySizeMultiplier)))
    img = cvzone.overlayPNG(img, overlayResize, [int(box[0] + (overlayResize.shape[0] * xMultiplier)),
                                                 int(box[1] + (overlayResize.shape[1] * yMultiplier))])


def apply(img: Union[np.ndarray, None], selectedFilter: str) -> bool:
    overlay = cv2.imread(selectedFilter, cv2.IMREAD_UNCHANGED)
    detector = cv2.FaceDetectorYN.create("face_detection_yunet_2023mar.onnx", "", (0, 0))
    imgW = int(img.shape[1])
    imgH = int(img.shape[0])
    detector.setInputSize((imgW, imgH))
    # Getting detections
    _, detections = detector.detect(img)

    # if no faces detected, no point continuing
    if detections is None:
        return False

    # parameters: x1, y1, w, h, x_le, y_le, x_re, y_re, x_nt, y_nt, x_rcm, y_rcm, x_lcm, y_lcm
    for face in detections:
        # get the first 4 params, not interested in rest and put it into a list
        box = list(map(int, face[:4]))
        landmarks = list(map(int, face[4:len(face) - 1]))
        nose = [landmarks[4], landmarks[5]]
        leftEye = [landmarks[0], landmarks[1]]

        # cv2.rectangle(img, box, (0, 255, 0), 2)

        if "stache" in selectedFilter:
            resize_and_position_landmark(overlay, img, box, nose, 1, STACHE_Y_SIZE_MULTIPLIER,
                                         STACHE_X_MULTIPLIER,
                                         STACHE_Y_MULTIPLIER)
        elif "robber" in selectedFilter:
            resize_and_position_default(overlay, img, box, ROBBER_X_SIZE_MULTIPLIER,
                                        ROBBER_Y_SIZE_MULTIPLIER,
                                        ROBBER_X_MULTIPLIER,
                                        ROBBER_Y_MULTIPLIER)
        elif "medieval" in selectedFilter:
            resize_and_position_default(overlay, img, box, MEDIEVAL_X_SIZE_MULTIPLIER,
                                        MEDIEVAL_Y_SIZE_MULTIPLIER,
                                        MEDIEVAL_X_MULTIPLIER,
                                        MEDIEVAL_Y_MULTIPLIER)

        elif "gandalf" in selectedFilter:
            resize_and_position_default(overlay, img, box, GANDALF_X_SIZE_MULTIPLIER,
                                        GANDALF_Y_SIZE_MULTIPLIER,
                                        GANDALF_X_MULTIPLIER,
                                        GANDALF_Y_MULTIPLIER)
        elif "chill" in selectedFilter:
            # mouth
            overlay2 = cv2.imread('filters/chill2.png', cv2.IMREAD_UNCHANGED)
            resize_and_position_landmark(overlay, img, box, leftEye, CHILL_X_SIZE_MULTIPLIER,
                                         CHILL_Y_SIZE_MULTIPLIER,
                                         CHILL_X_MULTIPLIER,
                                         CHILL_Y_MULTIPLIER)
            resize_and_position_landmark(overlay2, img, box, nose, CHILL_X_SIZE_MULTIPLIER_MOUTH,
                                         CHILL_Y_SIZE_MULTIPLIER_MOUTH,
                                         CHILL_X_MULTIPLIER_MOUTH,
                                         CHILL_Y_MULTIPLIER_MOUTH)


        else:
            overlay_resize = cv2.resize(overlay, (box[2], box[3]))
            img = cvzone.overlayPNG(img, overlay_resize, [box[0], box[1]])

    save_image(img)

    cv2.imshow('Window', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return True


def save_image(img):
    cv2.imwrite('filtered_img.png', img)
