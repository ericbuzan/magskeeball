from .basic_skeeball import BasicSkeeball
from . import resources as res
import random


class Target(BasicSkeeball):

    intro_text = [
        "HIT THE TARGET TO",
        "SCORE 1000 POINTS!"
    ]

    def startup(self):
        self.bg_music = res.TARGET_SFX['TARGET_BG']
        self.bg_music.set_volume(0.25)
        self.bg_music.play()

        super(Target,self).startup()

        print("Special Mode: Target")
        self.persist['active_game_mode'] = 'TARGET'
        self.ball_bonuses= []
        self.got_bonus = 'idle'
        self.bonus = [100,200,200,300,300,300,400,400,500]
        random.shuffle(self.bonus)
        self.playing_outro = False


    def update(self):
        super(Target,self).update()
        if self.got_bonus != 'idle':
            if (self.ticks - self.ticks_last_ball) >= 2*res.FPS:
                self.got_bonus = 'idle'
        if self.balls == 0 and not self.playing_outro:
            self.bg_music.stop()
            res.TARGET_SFX['COMPLETE'].play()

    def handle_event(self,event):
        if event.button == res.B.QUIT:
            self.quit = True
        if self.balls == 0:
            return 
        if event.down and event.button in res.POINTS:
            self.add_score(res.POINTS[event.button])
        if event.down and event.button == res.B.RETURN:
            self.returned_balls-=1
            if self.returned_balls < self.balls:
                self.add_score(0)
        if event.button == res.B.CONFIG:
            self.balls = 0
            self.returned_balls = 0


    def add_score(self,score):
        self.ball_scores.append(score)
        self.balls-=1
        if self.ball_scores[-1] == self.bonus[8-self.balls]:
            self.score_buffer += 1000
            self.got_bonus = 'yes'
            self.ball_bonuses.append(True)
            res.TARGET_SFX['TARGET_HIT'].play()
        else:
            self.score_buffer += score
            self.got_bonus = 'no'
            self.ball_bonuses.append(False)
            res.TARGET_SFX['TARGET_MISS'].play()
        self.advance_score = True
        #if self.balls in [3,6]:
        #    self.sensor.release_balls()
        self.ticks_last_ball = self.ticks

    def draw_panel(self,panel):
        panel.clear() 
        d = 6 if self.debug else 0
        panel.draw.text((34-d, 31), "%d" % self.balls,font=res.FONTS['Digital14'],fill=res.BALL_COLORS[self.balls])
        panel.draw.text((17-d, 4), "%04d" % self.score ,font=res.FONTS['Digital16'],fill=res.COLORS['PURPLE'])
        panel.draw.text((8-d,31), "BALL" ,font=res.FONTS['Medium'],fill=res.BALL_COLORS[self.balls])
        panel.draw.text((8-d,41), "LEFT" ,font=res.FONTS['Medium'],fill=res.BALL_COLORS[self.balls])
        panel.draw.text((52-d,31), "TARGET" ,font=res.FONTS['Medium'],fill=res.COLORS['YELLOW'])
        if self.balls > 0:
            panel.draw.text((61-d,41), str(self.bonus[9-self.balls]) ,font=res.FONTS['Medium'],fill=res.COLORS['YELLOW'])
        if self.got_bonus == 'yes':
            panel.draw.text((16-d,53), "BONUS! 1000" ,font=res.FONTS['Medium'],fill=res.COLORS['WHITE'])
        if self.got_bonus == 'no':
            panel.draw.text((27-d,53), "MISSED!" ,font=res.FONTS['Medium'],fill=res.COLORS['WHITE'])
        if self.debug:
            for i,(num,b) in enumerate(zip(self.ball_scores,self.ball_bonuses)):
                num = str(num)
                t = 4*len(num)
                color = res.COLORS['WHITE'] if b else res.COLORS['RED']
                panel.draw.text((96-t,1+6*i),num,font=res.FONTS['Tiny'],fill=color)
            panel.draw.text((90,57), "%d" % self.returned_balls,font=res.FONTS['Small'],fill=res.COLORS['ORANGE'])

    #def cleanup(self):
    #    super(Target,self).cleanup()
