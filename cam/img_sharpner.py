from image_processor import ImageProcessor
import numpy as np
import cv2


class ImageSharpener(ImageProcessor):

    def __init__(self, cam, input_img):
        super().__init__(cam)
        self.input_img = input_img
        self.kernel_size = 5
        self.sigma = 1.0
        self.amount = 1.0

    def get_output(self):
        # Convert to float to avoid overflow or underflow losses.
        output = self.input_img.astype(np.float32)

        # Apply unsharp mask filter
        blurred = cv2.GaussianBlur(output, (self.kernel_size, self.kernel_size), self.sigma)
        output = cv2.addWeighted(output, 1 + self.amount, blurred, -self.amount, 0)

        # Convert back to uint8
        output = np.clip(output, 0, 255)
        output = output.astype(np.uint8)

        return output
