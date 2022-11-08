from image_processor import ImageProcessor
import numpy as np
import cv2


class ImageSharpener(ImageProcessor):

    def __init__(self, cam, input_img):
        super().__init__(cam)
        self.input_img = input_img

    def get_output(self):
        print("Sharpening image")
        sharpen_filter = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        sharped_img = cv2.filter2D(self.input_img, -1, sharpen_filter)

        return sharped_img
