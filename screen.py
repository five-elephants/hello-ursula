from neopixel import *

LED_PIN = 18

OFFSCREEN_COUNT = 1
SCREEN_SZ_X = 17
SCREEN_SZ_Y = 17

class CoordinateException(Exception):
    def __init__(self):
        pass

def xy(x, y):
    if x < 0 or x >= SCREEN_SZ_X:
        raise CoordinateException()

    if y < 0 or y >= SCREEN_SZ_Y:
        raise CoordinateException()

    if ((y < 14) and (y % 2 == 0)) or ((y >= 14) and (y % 2 == 1)):
        xoff = SCREEN_SZ_X - x -1
    else:
        xoff = x
    rv = OFFSCREEN_COUNT + (y * SCREEN_SZ_X) + xoff

    if rv < OFFSCREEN_COUNT or rv >= OFFSCREEN_COUNT + (SCREEN_SZ_X * SCREEN_SZ_Y):
        raise CoordinateException()

    return rv


class Screen(object):
    def __init__(self, brightness=80):
        self.screen = Adafruit_NeoPixel(num = OFFSCREEN_COUNT + (SCREEN_SZ_X * SCREEN_SZ_Y),
                                        pin = LED_PIN,
                                        brightness = brightness)
        self.screen.begin()


    def clr(self, color=Color(0, 0, 0)):
        for i in range(self.screen.numPixels()):
            self.screen.setPixelColor(i, color)
        self.screen.show()

    def set(self, i, color):
        self.screen.setPixelColor(i, color)
        self.screen.show()

    def image(self, bitmap, coord_transform, color_transform):
        self.clr()
        for a,row in enumerate(bitmap):
            for b,pixel in enumerate(row):
                self.screen.setPixelColor(coord_transform(a, b), color_transform(pixel))
        self.screen.show()

    def show(self):
        self.screen.show()