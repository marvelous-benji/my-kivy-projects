from kivy.properties import Clock
from kivy.core import window
from kivymd.app import MDApp
from datetime import datetime
from kivy.properties import ObjectProperty
from kivymd.uix.boxlayout import MDBoxLayout




class Timer(MDBoxLayout):
    timer1 = ObjectProperty(None)
    timer2 = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    player1_turn = True
    player2_turn = False
    Time_In_Milli1 = 120000
    Time_In_Milli2 = 120000
    player_before_pause = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_touch_down(self, touch):
        if self.ids.pause_btn.text == "Play":
            return super().on_touch_down(touch)
        if self.player1.collide_point(*touch.pos):
            self.player1_turn = False
            self.player2_turn = True
        elif self.player2.collide_point(*touch.pos):
            self.player2_turn = False
            self.player1_turn = True
        return super().on_touch_down(touch)

    def update_time(self,min,sec,mili_sec):
        if self.player1_turn:   
            self.timer1.text = "%s:%s.[sub]%s[/sub]"%(min,sec,mili_sec)
        elif self.player2_turn:
            self.timer2.text = "%s:%s.[sub]%s[/sub]"%(min,sec,mili_sec)
        else:
            return

    def pause_timer(self):
        print('You called')
        if self.ids.pause_btn.text == "Pause":
            self.player_before_pause = 'player1' if self.player1_turn else 'player2'
            self.player1_turn = False
            self.player2_turn = False
            self.ids.pause_btn.text = "Play"
        elif self.ids.pause_btn.text == "Play":
            self.ids.pause_btn.text = "Pause"
            if self.player_before_pause == 'player1':
                self.player1_turn = True
            else:
                self.player2_turn = True
        else:
            return

    def reset_timer(self):
        self.Time_In_Milli1 = 120000
        self.Time_In_Milli2 = 120000
        self.timer1.text = "%s:%s.[sub]%s[/sub]"%("2","00","000")
        self.timer2.text = "%s:%s.[sub]%s[/sub]"%("2","00","000")
        return

class WatchApp(MDApp):
    Time_In_Milli = 0

    def build(self):
        self.chess_timer = Timer()
        return self.chess_timer
    
    def update_timer(self,*args):
        if self.chess_timer.player2_turn or self.chess_timer.player1_turn:
            if self.chess_timer.Time_In_Milli1 == 0 or self.chess_timer.Time_In_Milli2 == 0:
                return False
            if self.chess_timer.player1_turn:
                self.chess_timer.Time_In_Milli1 -= 1
                self.Time_In_Milli = self.chess_timer.Time_In_Milli1
            elif self.chess_timer.player2_turn:
                self.chess_timer.Time_In_Milli2 -= 1
                self.Time_In_Milli = self.chess_timer.Time_In_Milli2
            milli = int(self.Time_In_Milli % 1000)
            total_seconds = int(self.Time_In_Milli // 1000)
            mins = int(total_seconds // 60)
            seconds = int(total_seconds % 60)
            self.chess_timer.update_time(mins,seconds,milli)
        return
    
    def on_start(self):
        Clock.schedule_interval(self.update_timer,1/1000)
        return super().on_start()





if __name__ == '__main__':
    from kivy.core.text import LabelBase
    #from kivy.core.window import Window

    #Window.size = (720,310)
    LabelBase.register(name='Oxygen',
                        fn_bold='Oxygen-Regular.ttf',
                        fn_regular='Oxygen-Light.ttf')
    WatchApp().run()