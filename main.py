import kivy.graphics

from game import Game
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock


class BattleSheep(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game = Game(self.canvas)
        Clock.schedule_interval(self.frame, 1 / self.game.fps)

    def frame(self, dt):
        self.game.frame()


class BattleSheepApp(App):
    def build(self):
        return BattleSheep()


if __name__ == '__main__':
    app = BattleSheepApp()
    app.run()
