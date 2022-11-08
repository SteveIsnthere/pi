import time
from img_drboost import ImageDynamicRangeBooster
from setup import *
from PIL import Image
from img_stacker import ImageStacker
from img_sharpner import ImageSharpener

total_image = 50
size = 50

camera.exposure_mode = 'night'
camera.sensor_mode = 3
camera.iso = 0
camera.resolution = (32 * size, 16 * size)
camera.framerate_range = (0.0167, 60)
time.sleep(5)

output = ImageDynamicRangeBooster(camera, ImageStacker(camera, total_image).get_output()).get_output()

img = Image.fromarray(ImageSharpener(camera, output).get_output(), 'RGB')
img.save('final.png')
print("done")
