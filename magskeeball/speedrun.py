from .state import GameMode
from . import resources as res
import random
import time


class Speedrun(GameMode):

    has_high_scores = True
    intro_text = [
        "HOW FAST CAN YOU",
        "SCORE 5000 POINTS?"
    ]

    def startup(self):
        self.score = 0
        self.score_buffer = 0
        self.advance_score = False

        self.balls = 0
        self.returned_balls = 0
        self.ball_scores = []

        self.time_elapsed = -2

        self.persist['active_game_mode'] = 'TIMED'

    def handle_event(self,event):
        if event.button == res.B.QUIT:
            self.quit = True
        if self.time_elapsed < 0:
            return
        if event.down and event.button in res.POINTS:
            self.add_score(res.POINTS[event.button])
            res.SOUNDS[event.button.name].play()
        if event.down and event.button == res.B.RETURN:
            self.returned_balls+=1
            if self.returned_balls > self.balls:
                self.add_score(0)
                res.SOUNDS['MISS'].play()
        if event.button == res.B.CONFIG:
            self.time_elapsed = 599.0

    def update(self):
        if self.advance_score:
            if self.score_buffer > 0:
                self.score += 100
                self.score_buffer -= 100
        if self.score_buffer == 0:
            self.advance_score = False
        if self.score >= 5000:
            if not self.advance_score:
                self.manager.next_state = "HIGHSCORE"
                self.done = True
        else:
            self.time_elapsed += 1 / res.FPS
        if self.time_elapsed >= 599.0:
            self.manager.next_state = "HIGHSCORE"
            self.done = True

    def draw_panel(self,panel):
        panel.clear()
        if self.time_elapsed < 0:
            display_time = 0.0
        else:
            display_time = self.time_elapsed

        minutes = int(display_time / 60)
        seconds = int(display_time % 60)
        fraction = 5*int(display_time % 1 * 20)

        panel.draw.text((7, 6), "%01d" % minutes, font=res.FONTS['Digital14'], fill=res.COLORS['PURPLE'])
        panel.draw.text((28, 6), "%02d" % seconds, font=res.FONTS['Digital14'], fill=res.COLORS['PURPLE'])
        panel.draw.text((63, 6), "%02d" % fraction, font=res.FONTS['Digital14'], fill=res.COLORS['PURPLE'])
        panel.draw.rectangle([21, 18, 24, 21],fill=res.COLORS['PURPLE'])
        panel.draw.rectangle([21, 9, 24, 12],fill=res.COLORS['PURPLE'])
        panel.draw.rectangle([56, 21, 59, 24],fill=res.COLORS['PURPLE'])
        panel.draw.text((57,31), "BALLS" ,font=res.FONTS['Medium'],fill=res.COLORS['YELLOW'])
        panel.draw.text((66, 41), "%02d" % self.balls,font=res.FONTS['Medium'],fill=res.COLORS['YELLOW'])

        panel.draw.text((9,31), "SCORE",font=res.FONTS['Medium'],fill=res.COLORS['GREEN'])
        panel.draw.text((12, 41), "%04d" % self.score,font=res.FONTS['Medium'],fill=res.COLORS['GREEN'])


        if self.time_elapsed < 0:
            panel.draw.text((9,54), "READY... {:03.1f}".format(-self.time_elapsed),font=res.FONTS['Medium'],fill=res.COLORS['WHITE'])
        elif self.time_elapsed < 2:
            panel.draw.text((39,54), "GO!",font=res.FONTS['Medium'],fill=res.COLORS['WHITE'])

    def cleanup(self):
        print("Pausing for 1 seconds")
        time.sleep(1)
        self.persist['last_score'] = self.score
        return

    def add_score(self,score):
        self.score_buffer += score
        self.ball_scores.append(score)
        self.balls+=1
        self.advance_score = True
        #if self.balls in [3,6]:
        #    self.sensor.release_balls()
