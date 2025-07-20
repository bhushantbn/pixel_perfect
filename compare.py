import cv2
from skimage.metrics import structural_similarity as ssim
import numpy as np
import os

def compare_images(imageA_path, imageB_path, output_path='output/diffs/diff.png'):
    imageA = cv2.imread(imageA_path)
    imageB = cv2.imread(imageB_path)

    if imageA.shape != imageB.shape:
        raise ValueError("Images must have the same dimensions")

    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

    (score, diff) = ssim(grayA, grayB, full=True)
    diff = (diff * 255).astype("uint8")

    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(output_path, imageB)

    return score, output_path