import time
from img_drboost import ImageDynamicRangeBooster
from setup import *
from img_stacker import ImageStacker
from helpers import save_image

total_image = 5
size = 50

camera.exposure_mode = 'night'
camera.sensor_mode = 3
camera.iso = 0
camera.resolution = (32 * size, 16 * size)
camera.framerate_range = (0.0167, 60)
time.sleep(5)

# output = ImageDynamicRangeBooster(camera, ImageStacker(camera, total_image).get_output()).get_output()
output = ImageStacker(camera, 1).get_output()
save_image(output, "output.jpg")
print("done")
