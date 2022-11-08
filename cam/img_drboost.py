from image_processor import ImageProcessor
import time
import numpy as np

from img_stacker import ImageStacker


class ImageDynamicRangeBooster(ImageProcessor):

    def __init__(self, cam, input_image):
        super().__init__(cam)
        self.input_image = input_image

    def get_overexpose_image(self):
        dimmest_pixel = 0
        self.cam.shutter_speed = 100000
        overexpose_img = self.generate_image_array(self.img_width, self.img_height)
        while dimmest_pixel < 4:
            self.cam.shutter_speed = int(self.cam.shutter_speed * 1.5)
            time.sleep(1)
            self.cam.capture(overexpose_img, 'rgb')
            dimmest_pixel = np.min(overexpose_img)
            if self.cam.shutter_speed >= 10000000 or np.mean(overexpose_img) > 200:
                break
        return ImageStacker(self.cam, 3).get_output()

    def get_underexpose_image(self):
        brightest_pixel = 255
        underexpose_img = self.generate_image_array(self.img_width, self.img_height)
        self.cam.shutter_speed = 150000
        while brightest_pixel > 249:
            self.cam.shutter_speed = int(self.cam.shutter_speed / 1.5)
            self.cam.capture(underexpose_img, 'rgb')
            brightest_pixel = np.max(underexpose_img)
            if self.cam.shutter_speed <= 1000 or np.mean(underexpose_img) < 25:
                break
        return ImageStacker(self.cam, 10).get_output()

    @staticmethod
    def get_out_of_expose_pixels(image):
        underexpose_pixels = []
        overexpose_pixels = []
        for row in range(len(image)):
            print(str(row / len(image) * 100) + "%")
            for col in range(len(image[row])):
                average = np.mean(image[row][col])
                if average > 235:
                    overexpose_pixels.append([row, col])
                if average < 14:
                    underexpose_pixels.append([row, col])

        return underexpose_pixels, overexpose_pixels

    def get_output(self):
        overexpose_img = self.get_overexpose_image()
        underexpose_img = self.get_underexpose_image()
        underexpose_pixels, overexpose_pixels = self.get_out_of_expose_pixels(self.input_image)

        for pixel in overexpose_pixels:
            self.input_image[pixel[0]][pixel[1]] = underexpose_img[pixel[0]][pixel[1]]

        for pixel in underexpose_pixels:
            self.input_image[pixel[0]][pixel[1]] = overexpose_img[pixel[0]][pixel[1]]

        return self.input_image
