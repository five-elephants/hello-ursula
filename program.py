#!/usr/bin/env python

from screen import *
from blit import *
from life import *
from clock import *
from s3_data import *
from ambient import *

from datetime import datetime,timedelta
import time
import os
import random
import configparser 
import json
import string
import re
from itertools import chain

class LifeMode(object):
    def __init__(self, cfg):
        if not cfg is None:
            self.step_dt = cfg.getfloat('LifeMode', 'step_dt')
            self.max_steps = cfg.getint('LifeMode', 'max_steps')
        else:
            self.step_dt = 0.6
            self.max_steps = 100
        self.life = Life()
        self.step(0.0)

    def step(self, dt):
        #print("Step {}".format(dt))
        self.img_clock = make_analog_clock_dither(datetime.now().time())
        self.life.step()
        if self.life.is_extinct() or self.life.static or self.life.n_step > self.max_steps:
            self.life = Life()

    def render(self, dt):
        img_life = self.life.render_transition(min(1.0, dt / self.step_dt))
        img = blit(img_life, self.img_clock, src_key=[0, 0, 0])
        return img

class StaticImgMode(object):
    def __init__(self, directory, cfg):
        if not cfg is None:
            self.step_dt = cfg.getfloat('StaticImgMode', 'step_dt')
        else:
            self.step_dt = 4.0
        self.directory = directory
        self.rng = random.Random()

    def step(self, dt):
        lst = list(filter(lambda x: x.endswith('.png'), os.listdir(self.directory)))
        sel = os.path.join(self.directory, lst[self.rng.randint(0, len(lst)-1)])
        self.bg_img = load_png_xy(sel)
        print('Selecting {}'.format(sel))

    def render(self, dt):
        img_clock = make_analog_clock_dither(datetime.now().time())
        img = blit(self.bg_img, img_clock, src_key=[0, 0, 0])
        return img

class S3ImgMode(StaticImgMode):
    def __init__(self, directory, cfg):
        super(S3ImgMode, self).__init__(directory, cfg)

        if not cfg is None:
            self.download_every = timedelta(minutes=cfg.getint('S3ImgMode', 'download_every'))
            self.text_scroll_speed = cfg.getfloat('S3ImgMode', 'text_scroll_speed')
        else:
            self.download_every = timedelta(minutes=10)
            self.text_scoll_speed = 0.2
        self.msg_fltr = re.compile(r'[^a-zA-Z0-9_\ ]+')
        self.last_download = datetime.now()
        download_all_to(self.directory)

    def step(self, dt):
        if datetime.now() > self.last_download + self.download_every:
            download_all_to(self.directory)
            self.last_download = datetime.now()

        def f(x):
            if x.endswith('.png'):
                key = x.split('.')[0]
                meta_fn = os.path.join(self.directory, 'meta_{}.json'.format(key))
                if os.path.exists(meta_fn):
                    return True
            return False


        #lst = filter(lambda x: x.endswith('.png'), os.listdir(self.directory))
        lst = list(filter(f, os.listdir(self.directory)))
        fn = lst[self.rng.randint(0, len(lst)-1)]
        sel = os.path.join(self.directory, fn)
        self.bg_img = load_png_xy(sel)

        key = fn.split('.')[0]
        meta_fn = os.path.join(self.directory, 'meta_{}.json'.format(key))
        if os.path.exists(meta_fn):
            print("Loading meta '{}'".format(meta_fn))
            with open(meta_fn) as f:
                data = json.load(f)
            #s = "{}: {}".format(data['name'], data['message'])
            s = self.msg_fltr.sub('', str(data['message']))
            self.txt_n_screens, self.txt_img = text(s, (0, 255, 0), offset=(SCREEN_SZ_X, 0))
            self.txt_scroll = 0.0
            self.have_message = True
            print("Have a message: '{}' by {}".format(s, data['name']))
        else:
            self.have_message = False

        print('Selecting {}'.format(sel))

    def render(self, dt):
        img = super(S3ImgMode, self).render(dt)

        if self.have_message:
            off = int(self.txt_scroll * SCREEN_SZ_X)
            #print('scroll: {}/{} => {} [{}]'.format(self.txt_scroll, self.txt_n_screens, off, self.txt_img.shape))
            img = blitxy(img, self.txt_img, (0, 12),
                    src_rect=(off, 0, SCREEN_SZ_X, self.txt_img.shape[1]),
                    src_key=[0, 0, 0])
            self.txt_scroll = self.text_scroll_speed * dt
            self.txt_scroll -= self.txt_n_screens * math.floor(self.txt_scroll / self.txt_n_screens) 

        return img



class Program(object):
    def __init__(self, cfg_file='dev.cfg'):
        self.cfg = configparser.ConfigParser()
        self.cfg.readfp(open(cfg_file))

        # configuration
        self.refresh_dt = 1.0/ self.cfg.getfloat('Program', 'refresh_rate')
        self.duration_secs = (self.cfg.getint('Program', 'duration_min'), self.cfg.getint('Program', 'duration_max'))
        self.ambient_light_control = self.cfg.getboolean('LightControl', 'ambient_light_control')
        self.light_control_dt = self.cfg.getfloat('LightControl', 'dt')
        self.light_control_kp = self.cfg.getfloat('LightControl', 'kp')
        self.light_control_range = (self.cfg.getint('LightControl', 'min'), self.cfg.getint('LightControl', 'max'))
        self.default_brightness = self.cfg.getint('LightControl', 'default_brightness')
        self.schedule = self.read_schedule(self.cfg.get('Program', 'schedule'))
        print("Configured schedule: {}".format(self.schedule))

        self.rng = random.Random()
        self.sense_light = LightSensor()
        self.scr = Screen(brightness=self.default_brightness)
        self.scr.clr()

        self.modes = [
                LifeMode(self.cfg),
                StaticImgMode('img', self.cfg),
                S3ImgMode('spool', self.cfg),
            ]

    def read_schedule(self, s):
        rv = []
        entries = s.split(',')

        for entry in entries:
            a,b = entry.split('-', maxsplit=1)
            rv.append((datetime.strptime(a, '%H:%M').time(),
                       datetime.strptime(b, '%H:%M').time()))

        return rv


    def check_schedule(self, t):
        for x in self.schedule:
            if t >= x[0] and t < x[1]:
                return True
        return False


    def time_to_next_schedule(self, t):
        schedule_dts_today = (datetime.combine(datetime.today(), i[0]) for i in self.schedule)
        tomorrow = datetime.today() + timedelta(days=1)
        schedule_dts_tomorrow = (datetime.combine(tomorrow, i[0]) for i in self.schedule)
        schedule_dts = chain(schedule_dts_today, schedule_dts_tomorrow)

        deltas = (i - t for i in schedule_dts)
        return min(filter(lambda x: x >= timedelta(0), deltas))


    def run_mode(self, mode, until):
        last_t = 0.0
        last_lc_t = 0.0
        while datetime.now() < until:
            cur_t = time.time()

            #print("cur_t = {:03.2}, last_t = {:03.2}, step_dt = {:03.2}, cur_t - last_t = {}".format(cur_t, last_t, mode.step_dt, cur_t - last_t))
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
            now = datetime.now()
            if self.check_schedule(now.time()):
                sel_mode_i = self.rng.randint(0, len(self.modes)-1)
                sel_duration_sec = self.rng.randint(self.duration_secs[0], self.duration_secs[1])

                print('Selecting mode {} for {} seconds'.format(sel_mode_i, sel_duration_sec))
                self.run_mode(self.modes[sel_mode_i],
                              datetime.now() + timedelta(seconds=sel_duration_sec))

                time.sleep(self.refresh_dt)
            else:
                self.scr.clr()
                dt = self.time_to_next_schedule(now).seconds
                print('Sleeping for {} seconds'.format(dt))
                time.sleep(dt)



def run_it():
    #pg = Program('prod.cfg')
    pg = Program('dev.cfg')
    #pg.run_mode(pg.modes[1], datetime.now() + timedelta(seconds=10))
    pg.run()
    pg.scr.clr()


if __name__ == '__main__':
    run_it()
