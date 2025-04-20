import pygame as pg
from Models.rocket import Rocket
from Models.word import Word

class GameRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.sprite_group = pg.sprite.Group()
        # Create rocket
        self.rocket = Rocket(screen.rect)
        self.sprite_group.add(self.rocket)

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
        # Draw black background
        self.screen.image.fill((0, 0, 0))
        
        # First draw enemies (words)
        words = [sprite for sprite in self.sprite_group if isinstance(sprite, Word)]
        for word in words:
            word.draw(self.screen.image)
        
        # Then draw other sprites (like rocket)
        other_sprites = [sprite for sprite in self.sprite_group if not isinstance(sprite, Word)]
        for sprite in other_sprites:
            self.screen.image.blit(sprite.image, sprite.rect) 