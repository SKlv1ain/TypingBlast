import pygame as pg

from Utils.config import ArgumentParser
from Utils.clock import Clock

from Views.screen import Screen

from Controllers.state_controller import StateController

class GameApp:
    def __init__(self, argv=None):
        args = ArgumentParser().parse_args(argv)
        pg.init()
        pg.mixer.init()

        self.clock = Clock(args.framerate)
        self.screen = Screen(args.size)
        self.state_controller = StateController(self.screen, self.clock)

    def run(self):
        self.state_controller.run()
        pg.quit()
        
     

if __name__ == '__main__': 
    app = GameApp()
    app.run()
