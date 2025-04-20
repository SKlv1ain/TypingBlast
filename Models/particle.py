import pygame as pg

class Particle(pg.sprite.Sprite):
    def __init__(self, *groups, size=None, color=None, ttl=None):
        super().__init__(*groups)
        if size is None:
            size = (1, 1)
        self.image = pg.Surface(size, pg.SRCALPHA)
        if color is None:
            color = (200, 200, 200, 125)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.x = self.y = 0
        self.vx = self.vy = 0
        self.ax = self.ay = 0
        self.t = 0
        if ttl is None:
            ttl = 60 * 3
        self.ttl = ttl

    def update(self, *args):
        self.vx += self.ax
        self.vy += self.ay
        self.x += self.vx
        self.y += self.vy
        self.rect.topleft = (self.x, self.y)
        self.t += 1
        if self.t > self.ttl:
            self.kill() 