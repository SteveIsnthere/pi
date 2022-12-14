import time
from cam.processing_pipelines.img_drboost import ImageDynamicRangeBooster
from cam.setup import *
from cam.processing_pipelines.img_stacker import ImageStacker
from cam.helpers import save_image


def get_highest_quality_image():
    total_image = 5
    size = 50

    camera.exposure_mode = 'night'
    camera.sensor_mode = 3
    camera.iso = 0
    camera.resolution = (32 * size, 16 * size)
    camera.framerate_range = (0.0167, 60)
    time.sleep(5)

    output = ImageDynamicRangeBooster(camera, ImageStacker(camera, total_image).get_output()).get_output()

    return output


def update_image():
    save_image(get_highest_quality_image(), saving_path, 70)
