import argparse

def tupint(s):
    """Convert string 'x,y' to tuple of integers (x,y)."""
    return tuple(map(int, s.split(',')))

class ArgumentParser(argparse.ArgumentParser):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_argument('--size', default='800,600', type=tupint)
        self.add_argument('--framerate', default=60) 