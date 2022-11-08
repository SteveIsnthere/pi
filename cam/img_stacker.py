from image_processor import ImageProcessor
from helpers import sharpen_image


class ImageStacker(ImageProcessor):
    def __init__(self, cam, stack_size):
        super().__init__(cam)
        self.stack_size = stack_size

    def get_output(self):
        print("Stacking " + str(self.stack_size) + " images")
        output = self.generate_float_image_array(self.img_width, self.img_height)

        image_taken = 0
        while image_taken < self.stack_size:
            new_img = self.generate_image_array(self.img_width, self.img_height)
            self.cam.capture(new_img, 'rgb')
            new_img.astype('float64')
            new_img_portion = 1 - image_taken / self.stack_size
            output = output * (1 - new_img_portion) + new_img * new_img_portion
            image_taken += 1
            print(str(round(image_taken / self.stack_size * 100)) + "%")

        output = output.astype('uint8')

        return sharpen_image(output)
