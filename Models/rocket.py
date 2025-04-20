import pygame as pg
from pathlib import Path

class Rocket(pg.sprite.Sprite):
    def __init__(self, screen_rect):
        super().__init__()
        # Load rocket image
        image_path = Path("assets/images/rocket.png")
        if image_path.exists():
            self.image = pg.image.load(str(image_path))
            # Scale image if needed
            self.image = pg.transform.scale(self.image, (50, 50))  # ปรับขนาดตามต้องการ
        else:
            # Create a default rocket shape if image not found
            self.image = pg.Surface((30, 40))
            self.image.fill((200, 200, 200))
        
        self.rect = self.image.get_rect()
        
        # Position rocket at bottom center
        self.rect.centerx = screen_rect.centerx
        self.rect.bottom = screen_rect.bottom - 10  # เว้นระยะห่างจากขอบล่าง 10 pixels 