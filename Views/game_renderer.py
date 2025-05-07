import pygame as pg
from Models.rocket import Rocket
from Models.word import Word
import random

class GameRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.sprite_group = pg.sprite.Group()
        
        self.rocket = Rocket(screen.rect)
        self.sprite_group.add(self.rocket)
        
        self.stars = [(random.randint(0, self.screen.image.get_width()),
               random.randint(0, self.screen.image.get_height()))
              for _ in range(150)]


    def add_sprite(self, sprite):
        self.sprite_group.add(sprite)

    def add_sprites(self, sprites):
        self.sprite_group.add(*sprites)

    def remove_sprite(self, sprite):
        self.sprite_group.remove(sprite)

    def clear(self):
        self.sprite_group.empty()
        # Re-add rocket after clearing
        self.sprite_group.add(self.rocket)

    def update(self):
        self.sprite_group.update()
        
    def draw(self):
    # Animated space background
        self.screen.image.fill((10, 10, 25))  # dark navy instead of black

        # Animate and draw starfield
        new_stars = []
        for x, y in self.stars:
            y += 1  # constant downward motion
            if y > self.screen.image.get_height():
                y = 0
                x = random.randint(0, self.screen.image.get_width())
            pg.draw.circle(self.screen.image, (200, 200, 255), (x, y), 1)
            new_stars.append((x, y))
        self.stars = new_stars

        # Draw enemies (words)
        words = [sprite for sprite in self.sprite_group if isinstance(sprite, Word)]
        for word in words:
            word.draw(self.screen.image)

        # Draw other sprites (rocket, etc.)
        other_sprites = [sprite for sprite in self.sprite_group if not isinstance(sprite, Word)]
        for sprite in other_sprites:
            self.screen.image.blit(sprite.image, sprite.rect)
