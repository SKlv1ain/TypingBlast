# === Fixed word.py: delegate collision detection to GameController ===
import pygame as pg
import math
from .letter import Letter
from Utils.layout import align, wrap

class Word:
    def __init__(self, letters, target_pos, speed=0.5):
        self.original = letters
        self.letters = self.original
        self.sprites = list(map(Letter, self.letters))
        self.y = 0
        self.align()

        # coordinates for the target position
        self.target_x, self.target_y = target_pos

        # position and direction
        self.x = self.sprites[0].rect.x if self.sprites else 0
        self.y = self.sprites[0].rect.y if self.sprites else 0
        self.dx = 0
        self.dy = 0

        # speed settings 
        self.normal_speed = speed
        self.typing_speed = 0.5
        self.current_speed = self.normal_speed

        # countdown timer and reset delay
        self.reset_timer = 0
        self.reset_delay = 30

        # state variables
        self.is_being_typed = False
        self.already_destroyed = False 

        self.calculate_direction()


    def calculate_direction(self):
        if not self.sprites:
            return

        rect = self.rect()
        current_x, current_y = rect.center
        dx = self.target_x - current_x
        dy = self.target_y - current_y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance < 50:
            self.current_speed *= 0.9

        if distance == 0:
            self.dx = 0
            self.dy = 0
            return

        self.dx = dx / distance
        self.dy = dy / distance

    def align(self):
        align(self.rects(), left='right', top='top')

    def is_alive(self):
        return bool(self.letters)

    def is_hit(self, letter):
        return self.letters and letter.lower() == self.letters[0].lower()

    def rect(self):
        return wrap(self.rects())

    def rects(self):
        return tuple(sprite.rect for sprite in self.sprites)

    def shoot(self, letter):
        if not self.is_hit(letter):
            return False

        self.last_position = self.rect().center
        self.letters = self.letters[1:]
        self.sprites[0].kill()
        self.sprites.pop(0)

        self.current_speed = max(self.typing_speed, self.current_speed * 0.8)
        self.reset_timer = 0
        return True


    def get_target_position(self):
        if self.sprites:
            return self.rect().center
        return self.last_position

    def update(self):
        if not self.sprites:
            return

        self.reset_timer += 1
        if self.reset_timer >= self.reset_delay:
            self.current_speed = self.normal_speed

        self.calculate_direction()
        movement_x = self.dx * self.current_speed
        movement_y = self.dy * self.current_speed

        if abs(movement_x) < 0.01:
            movement_x = 0
        if abs(movement_y) < 0.01:
            movement_y = 0

        if movement_x != 0 or movement_y != 0:
            first_sprite = self.sprites[0]
            first_sprite.rect.x += movement_x
            first_sprite.rect.y += movement_y
            self.align()
            
        

    def explode(self):
        self.letters = ""
        for sprite in self.sprites:
            sprite.kill()
        self.sprites.clear()
        self.already_destroyed = True  

    def get_sprites(self):
        return self.sprites

    def draw(self, surface):
        if hasattr(self, 'enemy_image'):
            rect = self.rect()
            enemy_rect = self.enemy_image.get_rect()
            enemy_rect.center = rect.center
            surface.blit(self.enemy_image, enemy_rect)
            pg.draw.rect(surface, (255, 0, 0), enemy_rect, 1)
        else:
            print("No enemy image")

        for sprite in self.sprites:
            surface.blit(sprite.image, sprite.rect)