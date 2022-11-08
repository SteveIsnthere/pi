import numpy as np
import cv2


def sharpen_image(input_img):
    print("Sharpening image")
    sharpen_filter = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharped_img = cv2.filter2D(input_img, -1, sharpen_filter)

    return sharped_img


def save_image(img, name):
    cv2.imwrite(name, img)
