import board
import adafruit_bmp3xx

sensor = adafruit_bmp3xx.BMP3XX_I2C(board.I2C())

sensor.pressure_oversampling = 8
sensor.temperature_oversampling = 2
