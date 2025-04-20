import pygame as pg

class Screen:
    def __init__(self, size):
        self.image = pg.display.set_mode(size)
        self.background = self.image.copy()
        self.rect = self.image.get_rect()

    def clear(self):
        self.image.blit(self.background, (0, 0))

    def flip(self):
        pg.display.flip()

    def update(self):
        self.flip() 