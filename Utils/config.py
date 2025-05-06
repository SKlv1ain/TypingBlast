from Utils.settings import DEFAULT_SCREEN_SIZE, DEFAULT_FRAMERATE
import argparse

def tupint(s):
    return tuple(map(int, s.split(',')))

class ArgumentParser(argparse.ArgumentParser):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_argument('--size', default=f"{DEFAULT_SCREEN_SIZE[0]},{DEFAULT_SCREEN_SIZE[1]}", type=tupint)
        self.add_argument('--framerate', default=DEFAULT_FRAMERATE, type=int)
