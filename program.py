from screen import *
from blit import *
from life import *
from clock import *
from s3_data import *
from ambient import *

import datetime
import time

class LifeMode(object):
    def __init__(self):
        self.step_dt = 0.6
        self.life = Life()
        self.step(0.0)

    def step(self, dt):
        print("Step {}".format(dt))
        self.img_clock = make_analog_clock_dither(datetime.datetime.now().time())
        self.life.step()
        if self.life.is_extinct() or self.life.static or self.life.n_step > 100:
            self.life = Life()

    def render(self, dt):
        img_life = self.life.render_transition(min(1.0, dt / self.step_dt))
        img = blit(img_life, self.img_clock, src_key=[0, 0, 0])
        return img


class Program(object):
    def __init__(self):
        self.sense_light = LightSensor()
        self.scr = Screen()
        self.scr.clr()

        self.modes = [
                LifeMode(),
            ]

    def run_mode(self, mode, until):
        last_t = 0.0
        while datetime.datetime.now() < until:
            cur_t = time.time()

            if cur_t - last_t > mode.step_dt:
                mode.step(cur_t - last_t)
                last_t = cur_t

            img = mode.render(cur_t - last_t)
            self.scr.image(img, xy, color_map_watch)



def run_it():
    pg = Program()
    pg.run_mode(pg.modes[0], datetime.datetime.now() + datetime.timedelta(seconds=10))
    pg.scr.clr()


if __name__ == '__main__':
    run_it()
