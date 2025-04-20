import pygame as pg
from pathlib import Path
import math

class Bullet(pg.sprite.Sprite):
    def __init__(self, start_pos, target_pos):
        super().__init__()
        
        # Load bullet image
        image_path = Path("assets/images/bullet.png").absolute()
        if image_path.exists():
            try:
                self.image = pg.image.load(str(image_path)).convert_alpha()
                # Resize bullet to be smaller
                self.image = pg.transform.scale(self.image, (20, 20))
            except Exception as e:
                print(f"Failed to load bullet image: {e}")
                # Use a circle if loading fails
                self.image = pg.Surface((10, 10), pg.SRCALPHA)
                pg.draw.circle(self.image, (255, 255, 0), (5, 5), 5)
        else:
            print("Bullet image not found, using circle instead")
            # Use a circle if file not found
            self.image = pg.Surface((10, 10), pg.SRCALPHA)
            pg.draw.circle(self.image, (255, 255, 0), (5, 5), 5)
        
        # Create rect and set starting position
        self.rect = self.image.get_rect()
        if not self.rect:
            print("Could not create rect")
            self.kill()
            return
            
        self.rect.center = start_pos
        
        # Calculate direction and speed
        self.speed = 10
        dx = target_pos[0] - start_pos[0]
        dy = target_pos[1] - start_pos[1]
        distance = math.sqrt(dx * dx + dy * dy)
        
        if distance == 0:
            self.dx = 0
            self.dy = 0
        else:
            self.dx = (dx / distance) * self.speed
            self.dy = (dy / distance) * self.speed
        
        # Store float positions for accuracy
        self.float_x = float(self.rect.x)
        self.float_y = float(self.rect.y)
        
        # Store target position for proximity check
        self.target_pos = target_pos
    
    def update(self):
        if not self.rect:
            self.kill()
            return
            
        # Move in the calculated direction
        self.float_x += self.dx
        self.float_y += self.dy
        self.rect.x = int(self.float_x)
        self.rect.y = int(self.float_y)
        
        # Check if target is reached (close enough)
        current_pos = self.rect.center
        dx = self.target_pos[0] - current_pos[0]
        dy = self.target_pos[1] - current_pos[1]
        distance = math.sqrt(dx * dx + dy * dy)
        
        if distance < 20:  # Remove bullet if close enough to target
            self.kill()