import cv2
import cvzone
import numpy as np
from typing import Union


def load_image(img: bytes) -> Union[np.ndarray, None]:
    # decode to a readable format for OpenCV
    imageArray = np.frombuffer(img, np.uint8)
    decodedImage = cv2.imdecode(imageArray, cv2.IMREAD_COLOR)

    if decodedImage is None:
        print("Discord Attachment image cannot be decoded")
        return

    print(decodedImage.shape)
    return decodedImage


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

    # parameters: x1, y1, w, h, x_re, y_re, x_le, y_le, x_nt, y_nt, x_rcm, y_rcm, x_lcm, y_lcm
    for face in detections:
        # get the first 4 params, not interested in rest and put it into a list
        box = list(map(int, face[:4]))

        cv2.rectangle(img, box, (0, 255, 0), 2)
        if "gandalf" in selectedFilter:
            overlay_resize = cv2.resize(overlay, (int(box[2] * 2), int(box[3] * 2)))
            img = cvzone.overlayPNG(img, overlay_resize, [box[0]-100, box[1]-30])
        else:
            overlay_resize = cv2.resize(overlay, (box[2], box[3]))
            img = cvzone.overlayPNG(img, overlay_resize, [box[0], box[1]])



    cv2.imshow('bruh', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return True
