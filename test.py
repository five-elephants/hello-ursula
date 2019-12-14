from screen import *
import clock
import datetime
import time
import numpy as np
from blit import blit,load_png,load_png_xy
from life import *
import os
import s3_data
import ambient


def test_border():
    scr = Screen()
    scr.clr()

    c = (20, 0, 0)

    for x in range(17):
        scr.set(xy(x, 0), c)
        scr.set(xy(x, 16), c)

    for y in range(17):
        scr.set(xy(0, y), c)
        scr.set(xy(16, y), c)

def test_image():
    image = [
            [ 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456 ],
            [ 0x123456, 0xff0000, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456 ],
            [ 0x123456, 0x0000ff, 0x00ff00, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456 ],
            [ 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456 ],
            [ 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456 ],
            [ 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456 ],
            [ 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456 ],
            [ 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456 ],
            [ 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456 ],
            [ 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456 ],
            [ 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456 ],
            [ 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456 ],
            [ 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456 ],
            [ 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456 ],
            [ 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456 ],
            [ 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456 ],
            [ 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456, 0x123456 ],
        ]

    scr = Screen()
    scr.clr()
    scr.image(image, xy, color_map_rgb)


def test_watch():
    scr = Screen()
    scr.clr()

    bg = np.zeros((17, 17, 3), dtype=np.uint8)
    bg[:,:,0] = 10

    for hour in range(12):
        for minute in range(60):
            t = datetime.time(hour, minute)
            watch = clock.make_analog_clock_dither(t)
            img = blit(bg, watch, src_key=np.array([0, 0, 0], dtype=np.uint8))
            #img = blit(bg, watch)
            scr.image(img, xy, clock.color_map_watch)
            time.sleep(0.05)

def test_png():
    s3_data.download_all_to('spool')

    scr = Screen()
    scr.clr()

    while True:
        for f in os.listdir('spool'):
            if f.endswith('.png'):
                print("Showing {}".format(f))
                img = np.array(load_png_xy(os.path.join('spool', f)) * 0.5, dtype=np.uint8)
                t = datetime.datetime.now().time()
                watch = clock.make_analog_clock_dither(t)
                buf = blit(img, watch, src_key=[0, 0, 0])
                scr.image(buf, xy, clock.color_map_watch)
                time.sleep(60)

def test_game_of_life():
    scr = Screen()
    scr.clr()

    life = Life()

    step_t = 0.6
    last_t = time.time()
    while True:
        t = datetime.datetime.now().time()
        watch = clock.make_analog_clock_dither(t)

        cur_t = time.time()
        if cur_t - last_t > step_t:
            life.step()
            if life.is_extinct() or life.static or life.n_step > 100:
                life = Life()

            bg = life.render_transition(0.0)
            last_t = cur_t
        else:
            bg = life.render_transition((cur_t - last_t) / step_t)

        img = blit(bg, watch, src_key=[0, 0, 0])
        scr.image(img, xy, clock.color_map_watch)
        time.sleep(1.0/60.0)

def test_light_control(kp=2.0):
    brightness = 20

    img = load_png_xy('spool/Sternennacht_17x17.png')
    sense = ambient.LightSensor()

    while True:
        scr = Screen(brightness)
        scr.image(img, xy, clock.color_map_watch)

        time.sleep(1.0)

        lum_sum, infra = sense.get_ambient_light()
        lum = lum_sum - infra
        brightness = max(0, min(255, int(kp * lum)))

        print('lum = {}, brightness = {}'.format(lum, brightness))

def test_blit():
    img_a = np.zeros((17, 17, 3), dtype=np.uint8)
    img_b = np.zeros((17, 17, 3), dtype=np.uint8)


    img_a[8,:,0] = 128
    img_b[:,8,1] = 128

    img = blit(img_a, img_b, src_key=[0, 0, 0])

    scr = Screen()
    scr.clr()
    scr.image(img, xy, clock.color_map_watch)


if __name__ == '__main__':
    #test_border()
    #test_image()
    #test_watch()
    #test_png()
    #test_game_of_life()
    #test_light_control()
    test_blit()
