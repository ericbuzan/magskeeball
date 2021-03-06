#!/usr/bin/env python3

import time
import sys
import os
from PIL import Image, ImageFont
import random

from .basic_skeeball import BasicSkeeball
from .combo import Combo
from .target import Target
from .dummy import Dummy
from .cricket import Cricket
from .config_menu import ConfigMenu
from .common import *
from . import panel
from . import sensor
from . import timer


HISCORE_COLORS = [
    COLORS.BLUE,
    COLORS.RED,
    COLORS.YELLOW,
    COLORS.GREEN,
    COLORS.PINK,
]

#test line change!

class SkeeballApp():

    def __init__(self):
        self.sensor = sensor.Sensor()
        self.panel = panel.Panel()
        
        self.basic_skeeball = BasicSkeeball(self.panel,self.sensor)
        self.combo = Combo(self.panel,self.sensor)
        self.target = Target(self.panel,self.sensor)
        self.dummy = Dummy(self.panel,self.sensor)
        self.cricket = Cricket(self.panel,self.sensor)
        self.game_list = [
            self.basic_skeeball,
            self.combo,
            self.target,
            self.dummy,
            self.cricket,
        ]
        self.game_dict = {g.name: g for g in self.game_list}
        

        self.config_menu = ConfigMenu(self.panel,self.sensor,self.game_list)
        self.settings = self.config_menu.settings
        self.do_red_hiscore = True
        self.attract_song = ATTRACT_MUSIC[random.choice(ATTRACT_MUSIC_KEYS)]

    def main_loop(self):
        self.clock = timer.Timer()
        #self.clock.ticks = 280
        while True:
            self.clock.tick(20)

            if self.clock.ticks % 400 < 200 or not(self.settings['do_hi_scores']):
                self.draw_attract()
            else:
                if self.clock.ticks % 800 < 400:
                    game = self.game_dict[self.settings['red_game']]
                else:
                    game = self.game_dict[self.settings['yellow_game']]
                self.draw_high_scores(game)
            if self.clock.ticks%2400 == 13:
                #play jingle once every 2 minutes if idle
                self.attract_song = ATTRACT_MUSIC[random.choice(ATTRACT_MUSIC_KEYS)]
                self.attract_song.play()
            self.sensor.update_buttons()
            if self.sensor.is_pressed(BUTTON['START']):
                self.attract_song.stop()
                self.game_dict[self.settings['red_game']].main_loop(self.settings)
                self.clock.ticks = 200
            elif self.sensor.is_pressed(BUTTON['SELECT']):
                self.attract_song.stop()
                self.game_dict[self.settings['yellow_game']].main_loop(self.settings)
                self.clock.ticks = 600
            elif self.sensor.is_pressed(BUTTON['CONFIG']):
                self.attract_song.stop()
                self.config_menu.main_loop()
                self.clock.ticks = 0

    def draw_attract(self):
        self.panel.clear()
        self.panel.paste(IMAGES['MainLogo'],(0,5))
        if self.clock.ticks % 40 < 30:
            self.panel.draw.text((15,54), "PRESS START",font=FONTS['Medium'],fill=COLORS.WHITE)
        self.panel.update()

    def draw_high_scores(self,game):
        self.panel.clear()
        title_text = 'HI SCORES - {}'.format(game.name)
        x = int(48-len(title_text)*2.5)+1
        self.panel.draw.text((x,2),title_text,font=FONTS['Small'],fill=COLORS.WHITE)
        (name,score) = game.high_scores[0]

        for i,(name,score) in enumerate(game.high_scores):
            if game.high_scores[0][1] > 9999:
                self.panel.draw.text((5+8*i,(i+1)*9),'{} {:5d}'.format(name,score),font=FONTS['Medium'],fill=HISCORE_COLORS[i])
            else:
                self.panel.draw.text((8+8*i,(i+1)*9),'{} {:4d}'.format(name,score),font=FONTS['Medium'],fill=HISCORE_COLORS[i])

        # self.panel.draw.text((24,10),'{} {}'.format(name,score),font=FONTS['Medium'],fill=HISCORE_COLORS[0])
        # for i in [1,2,3,4]:
        #     (name,score) = game.high_scores[i]
        #     self.panel.draw.text((28,i*8+12),'{} {}'.format(name,score),font=FONTS['Small'],fill=HISCORE_COLORS[i])

        if self.clock.ticks % 40 < 30:
            self.panel.draw.text((15,54), "PRESS START",font=FONTS['Medium'],fill=COLORS.WHITE)
        self.panel.update()
        #self.do_red_hiscore = not(self.do_red_hiscore)
    
    

def main():
    game = SkeeballApp()
    game.main_loop()

if __name__ == '__main__':
    main()
