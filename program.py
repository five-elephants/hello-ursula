#!/usr/bin/env python

from screen import *
from blit import *
from life import *
from clock import *
from s3_data import *
from ambient import *

import datetime
import time
import os
import random

class LifeMode(object):
    def __init__(self):
        self.step_dt = 0.6
        self.life = Life()
        self.step(0.0)

    def step(self, dt):
        #print("Step {}".format(dt))
        self.img_clock = make_analog_clock_dither(datetime.datetime.now().time())
        self.life.step()
        if self.life.is_extinct() or self.life.static or self.life.n_step > 100:
            self.life = Life()

    def render(self, dt):
        img_life = self.life.render_transition(min(1.0, dt / self.step_dt))
        img = blit(img_life, self.img_clock, src_key=[0, 0, 0])
        return img

class StaticImgMode(object):
    def __init__(self, directory):
        self.step_dt = 4.0
        self.directory = directory
        self.rng = random.Random()

    def step(self, dt):
        lst = filter(lambda x: x.endswith('.png'), os.listdir(self.directory))
        sel = os.path.join(self.directory, lst[self.rng.randint(0, len(lst)-1)])
        self.bg_img = load_png_xy(sel)
        print('Selecting {}'.format(sel))

    def render(self, dt):
        img_clock = make_analog_clock_dither(datetime.datetime.now().time())
        img = blit(self.bg_img, img_clock, src_key=[0, 0, 0])
        return img

class S3ImgMode(StaticImgMode):
    def __init__(self, directory):
        super(S3ImgMode, self).__init__(directory)

        self.download_every = datetime.timedelta(minutes=10)
        self.last_download = datetime.datetime.now()
        download_all_to(self.directory)

    def step(self, dt):
        if datetime.datetime.now() > self.last_download + self.download_every:
            download_all_to(self.directory)
            self.last_download = datetime.datetime.now()

        super(S3ImgMode, self).step(dt)



class Program(object):
    def __init__(self):
        # configuration
        self.duration_secs = (10, 60)
        self.ambient_light_control = True
        self.light_control_dt = 2.0
        self.light_control_kp = 2.0
        self.light_control_range = (10, 128)

        self.rng = random.Random()
        self.sense_light = LightSensor()
        self.scr = Screen()
        self.scr.clr()

        self.modes = [
                #LifeMode(),
                #StaticImgMode('img'),
                S3ImgMode('spool'),
            ]

    def run_mode(self, mode, until):
        last_t = 0.0
        last_lc_t = 0.0
        while datetime.datetime.now() < until:
            cur_t = time.time()

            if cur_t - last_t > mode.step_dt:
                mode.step(cur_t - last_t)
                last_t = cur_t

            img = mode.render(cur_t - last_t)
            self.scr.image(img, xy, color_map_watch)

            if self.ambient_light_control and cur_t - last_lc_t > self.light_control_dt:
                lum_sum, lum_infra = self.sense_light.get_ambient_light()
                lum = lum_sum - lum_infra
                brightness = max(self.light_control_range[0],
                                 min(self.light_control_range[1], int(self.light_control_kp * lum)))
                print('lum = {}, brightness = {}'.format(lum, brightness))
                self.scr.brightness(brightness)
                last_lc_t = cur_t


    def run(self):
        while True:
            sel_mode_i = self.rng.randint(0, len(self.modes)-1)
            sel_duration_sec = self.rng.randint(self.duration_secs[0], self.duration_secs[1])

            print('Selecting mode {} for {} seconds'.format(sel_mode_i, sel_duration_sec))
            self.run_mode(self.modes[sel_mode_i],
                          datetime.datetime.now() + datetime.timedelta(seconds=sel_duration_sec))



def run_it():
    pg = Program()
    #pg.run_mode(pg.modes[1], datetime.datetime.now() + datetime.timedelta(seconds=10))
    pg.run()
    pg.scr.clr()


if __name__ == '__main__':
    run_it()
