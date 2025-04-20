import pygame as pg
from Utils.game_utils import sprite2particles

class Letter(pg.sprite.Sprite):
    def __init__(self, letter, *groups):
        if len(letter) != 1:
            raise RuntimeError('letter must be length 1, got %r' % letter)
        super().__init__(*groups)
        self.letter = letter
        self.font = pg.font.Font(None, 32)
        self.image = self.font.render(str(letter), True, (200,200,200))
        self.rect = self.image.get_rect()

    def kill(self):
        particles = sprite2particles(self)
        for group in self.groups():
            group.add(*particles)
        super().kill() 