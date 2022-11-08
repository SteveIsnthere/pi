import time

import climage
from time import sleep
from picamera import PiCamera

width = 120
camera = PiCamera()
camera.resolution = (width, int(width/4*3))
camera.start_preview()
print("loading")
sleep(2)

while True:
    camera.capture('foo.jpg')
    output = climage.convert('foo.png', is_truecolor=True, is_256color=False, is_16color=False, is_8color=False,
                             width=width, palette="default")

    # prints output on console.
    print(output)
    time.sleep(1)