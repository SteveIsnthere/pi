import numpy as np
from abc import ABC, abstractmethod


class ImageProcessor(ABC):
    def __init__(self, cam):
        self.cam = cam
        self.img_height = self.cam.resolution.height
        self.img_width = self.cam.resolution.width

    @staticmethod
    def generate_image_array(x, y):
        return np.empty((y, x, 3), dtype=np.uint8)

    @staticmethod
    def generate_float_image_array(x, y):
        return np.empty((y, x, 3), dtype=np.float64)

    @abstractmethod
    def get_output(self):
        pass
