from cam.processing_pipelines.img_stacker import ImageStacker
from cam.processing_pipelines.image_processor import ImageProcessor
import numpy as np
import time
import cv2


class ImageHDR(ImageProcessor):

    def __init__(self, cam):
        super().__init__(cam)
        self.img_arr = []
        self.shutter_speeds_arr = []

    def get_overexpose_image(self):
        dimmest_pixel = 0
        self.cam.shutter_speed = 100000
        while dimmest_pixel < 4:
            self.cam.shutter_speed = int(self.cam.shutter_speed * 1.5)
            time.sleep(1)
            overexpose_img = ImageStacker(self.cam, 3).get_output()
            self.img_arr.append(overexpose_img)
            self.shutter_speeds_arr.append(self.cam.shutter_speed)
            dimmest_pixel = np.min(overexpose_img)
            if self.cam.shutter_speed >= 10000000 or np.mean(overexpose_img) > 200:
                break

    def get_underexpose_image(self):
        brightest_pixel = 255
        self.cam.shutter_speed = 150000
        while brightest_pixel > 249:
            self.cam.shutter_speed = int(self.cam.shutter_speed / 1.5)
            underexpose_img = ImageStacker(self.cam, 3).get_output()
            brightest_pixel = np.max(underexpose_img)
            self.img_arr.append(underexpose_img)
            self.shutter_speeds_arr.append(self.cam.shutter_speed)
            if self.cam.shutter_speed <= 1000 or np.mean(underexpose_img) < 25:
                break

    def get_output(self):
        shutter_speed = self.cam.shutter_speed
        base_image = ImageStacker(self.cam, 5).get_output()
        self.img_arr.append(base_image)
        self.shutter_speeds_arr.append(shutter_speed)
        self.get_underexpose_image()
        self.get_overexpose_image()
        self.shutter_speeds_arr = np.array(self.shutter_speeds_arr, dtype=np.float64)/1000000
        # Merge exposures to HDR image
        merge_debevec = cv2.createMergeDebevec()
        hdr_debevec = merge_debevec.process(self.img_arr, times=self.shutter_speeds_arr.copy())
        merge_robertson = cv2.createMergeRobertson()
        # Tone-map HDR image
        tone_map = cv2.createTonemap(gamma=2.2)
        res_debevec = tone_map.process(hdr_debevec.copy())
        # Exposure fusion using Mertens
        merge_mertens = cv2.createMergeMertens()
        res_mertens = merge_mertens.process(self.img_arr)
        # Convert datatype to 8-bit and save
        res_debevec_8bit = np.clip(res_debevec * 255, 0, 255).astype('uint8')
        res_mertens_8bit = np.clip(res_mertens * 255, 0, 255).astype('uint8')
        return res_debevec_8bit
