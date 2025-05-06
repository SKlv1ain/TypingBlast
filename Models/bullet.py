import pygame as pg
from pathlib import Path

class Bullet(pg.sprite.Sprite):
    SPEED = 10  
    RADIUS = 5  
    IMAGE = "assets/images/bullet.png" 
    
    def __init__(self, start_pos, target_pos):
        super().__init__()
        self.image = self._load_image(self.IMAGE, self.RADIUS)
        self.rect = self.image.get_rect(center=start_pos)

        # Vector-based movement for accuracy
        self.position = pg.Vector2(start_pos)
        self.target = pg.Vector2(target_pos)
        direction = self.target - self.position
        distance = direction.length()

        if distance == 0:
            self.velocity = pg.Vector2(0, 0)
        else:
            self.velocity = direction.normalize() * self.SPEED

    def _load_image(self, path, radius):
        image_file = Path(path).absolute()
        if image_file.exists():
            try:
                image = pg.image.load(str(image_file)).convert_alpha()
                return pg.transform.scale(image, (radius * 2, radius * 2))
            except Exception as e:
                print(f"Error loading bullet image: {e}")
                
                
        # Fallback to simple circle
        fallback = pg.Surface((radius * 2, radius * 2), pg.SRCALPHA)
        pg.draw.circle(fallback, (255, 255, 0), (radius, radius), radius)
        return fallback

    def update(self):
        self.position += self.velocity
        self.rect.center = self.position

        # Destroy bullet if close to the target
        if self.position.distance_to(self.target) < 20:
            self.kill()
