from setup import *
import time

while True:
    print(
        "Pressure: {:6.4f}  Temperature: {:5.2f}".format(sensor.pressure, sensor.temperature)
    )
    time.sleep(1)
