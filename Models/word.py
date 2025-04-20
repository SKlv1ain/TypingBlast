import pygame as pg
from pathlib import Path
from .letter import Letter
from Utils.game_utils import align, wrap
import math


class Word:
    def __init__(self, letters, target_pos):
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
        self.normal_speed = 1.5  # Normal speed (reduced from 3.0)
        self.typing_speed = 0.5  # Speed while typing (reduced from 1.0)
        self.current_speed = self.normal_speed
        
        # countdown timer and reset delay
        self.reset_timer = 0
        self.reset_delay = 30 
        
        # state variables
        self.is_being_typed = False
        
        # calculate initial direction
        self.calculate_direction()
        
        # Load enemy background image
        image_path = Path("assets/images/enemy.png").absolute()
        print(f"Loading file: {image_path}")
        print(f"File exists: {image_path.exists()}")
        
        if image_path.exists():
            try:
                self.enemy_image = pg.image.load(str(image_path)).convert_alpha()
                print("File loaded successfully")
                print(f"Original image size: {self.enemy_image.get_size()}")
                
                # Scale image much larger
                text_rect = self.rect()
                padding_x = 100
                padding_y = 50
                target_size = (text_rect.width + padding_x, text_rect.height + padding_y)
                self.enemy_image = pg.transform.scale(self.enemy_image, target_size)
                print(f"Resized image to: {target_size}")
                
                # Make enemy image more visible
                background = pg.Surface(target_size, pg.SRCALPHA)
                background.fill((100, 100, 100, 200))
                background.blit(self.enemy_image, (0, 0))
                self.enemy_image = background
                
                # Create surface for enemy with text
                for sprite in self.sprites:
                    sprite.image = sprite.font.render(sprite.letter, True, (255, 255, 255))
            except Exception as e:
                print(f"Error occurred: {e}")
                import traceback
                traceback.print_exc()
        else:
            print("enemy.png not found")

    def calculate_direction(self):
        """# Calculate direction to move toward the target"""
        if not self.sprites:
            return
            
        rect = self.rect()
        # Use the center of the rect to calculate direction
        current_x, current_y = rect.center
        target_x, target_y = self.target_x, self.target_y
        
        # Calculate distance along each axis
        dx = target_x - current_x
        dy = target_y - current_y
        
        # Calculate total distance
        distance = math.sqrt(dx * dx + dy * dy)
        
        # Slow down if very close to the target
        if distance < 50:
            self.current_speed *= 0.9
        
        if distance == 0:
            self.dx = 0
            self.dy = 0
            return
            
        # Normalize direction for movement
        self.dx = dx / distance
        self.dy = dy / distance

    def align(self):
        align(self.rects(), left='right', top='top')

    def is_alive(self):
        return bool(self.letters)

    def is_hit(self, letter):
        return self.letters and letter == self.letters[0]

    def rect(self):
        return wrap(self.rects())

    def rects(self):
        return tuple(sprite.rect for sprite in self.sprites)

    def shoot(self, letter):
        if not self.is_hit(letter):
            return False
        
        # Save current position before removing the letter
        self.last_position = self.rect().center
        
        self.letters = self.letters[1:]
        self.sprites[0].kill()
        self.sprites.pop(0)
        
        # Adjust speed when typed correctly, but don't go too slow
        self.current_speed = max(self.typing_speed, self.current_speed * 0.8)
        self.reset_timer = 0  # Reset the timer
        
        return True

    def get_target_position(self):
        """# If there are still letters left"""
        if self.sprites:  # ถ้ายังมีตัวอักษรเหลืออยู่
            return self.rect().center
        return self.last_position  # If no letters left, use last known position

    def update(self):
        if not self.sprites:
            return
            
        # Update timer and speed
        self.reset_timer += 1
        if self.reset_timer >= self.reset_delay:
            self.current_speed = self.normal_speed
            
        # Recalculate direction
        self.calculate_direction()
        
        # Compute movement
        movement_x = self.dx * self.current_speed
        movement_y = self.dy * self.current_speed
        
        # Check if movement is significant
        if abs(movement_x) < 0.01:
            movement_x = 0
        if abs(movement_y) < 0.01:
            movement_y = 0
            
        # Move according to calculated direction
        if movement_x != 0 or movement_y != 0:  # Move only when there is real change
            first_sprite = self.sprites[0]
            first_sprite.rect.x += movement_x
            first_sprite.rect.y += movement_y
            self.align()
        
        # Check for collision with rocket
        rect = self.rect()
        rocket_rect = pg.Rect(self.target_x - 30, self.target_y - 30, 60, 60)
        if rect.colliderect(rocket_rect):
            self.explode()

    def explode(self):
        """# Make the word disappear"""
        # Remove all letters
        self.letters = ""
        for sprite in self.sprites:
            sprite.kill()
        self.sprites.clear()

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

    def unlock(self):
        # This function is no longer called because unlock happens only after full typing
        pass