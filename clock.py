from datetime import time
import numpy as np
from screen import Color
import math

def color_map_watch(p):
    return Color(p[1], p[0], p[2])

def make_analog_clock(t):
    face = np.zeros((17, 17, 3), dtype=np.uint8)

    # hour hand
    for r in np.linspace(0.0, 8.0, 10):
        phi = (float(t.hour) / 12.0) * 2.0 * math.pi
        x = r * math.sin(phi) + 8.0
        y = r * math.cos(phi) + 8.0

        face[int(round(x, 0)), int(round(y, 0))] = [0, 0, 255]

    # minute hand
    for r in np.linspace(0.0, 6.0, 10):
        phi = (float(t.minute) / 60.0) * 2.0 * math.pi
        x = r * math.sin(phi) + 8.0
        y = r * math.cos(phi) + 8.0

        face[int(round(x, 0)), int(round(y, 0))] = [0, 255, 0]

    face[8, 8] = [255, 0, 0]

    return face

def make_analog_clock_dither(t):
    face = np.zeros((17, 17, 3), dtype=np.uint8)

    # hour hand
    for r in np.linspace(0.0, 5.0, 10):
        phi = (float(t.hour * 60 + t.minute) / (12.0 * 60.0)) * 2.0 * math.pi
        x = r * math.sin(phi) + 8.0
        y = r * math.cos(phi) + 8.0

        for fx, fy in [ (math.floor, math.floor),
                        (math.floor, math.ceil),
                        (math.ceil, math.floor),
                        (math.ceil, math.ceil) ]:
            ix = fx(x)
            iy = fy(y)
            d = max(0.0, 1.0 - math.sqrt((x - ix)**2 + (y - iy)**2))
            val = face[int(ix), int(iy)] + np.array([255, 255, 0]) * d
            face[int(ix), int(iy)] = np.clip(val, 0, 255)

    # minute hand
    for r in np.linspace(0.0, 8.0, 10):
        phi = (float(t.minute) / 60.0) * 2.0 * math.pi
        x = r * math.sin(phi) + 8.0
        y = r * math.cos(phi) + 8.0

        for fx, fy in [ (math.floor, math.floor),
                        (math.floor, math.ceil),
                        (math.ceil, math.floor),
                        (math.ceil, math.ceil) ]:
            ix = fx(x)
            iy = fy(y)
            d = max(0.0, 1.0 - math.sqrt((x - ix)**2 + (y - iy)**2))
            #d = math.exp(-5.0 * d)
            val = face[int(ix), int(iy)] + np.array([0, 255, 0]) * d
            face[int(ix), int(iy)] = np.clip(val, 0, 255)

    face[8, 8] = [255, 0, 0]

    return face
