import pygame as pg

class WaveView:
    def __init__(self):
        self.font = pg.font.Font(None, 64)
        self.timer = 0
        self.duration = 120  # 2 seconds

    def trigger(self):
        self.timer = self.duration

    def update(self):
        if self.timer > 0:
            self.timer -= 1

    def draw(self, surface, wave_number):
        if self.timer > 0:
            text = self.font.render(f"Wave {wave_number}", True, (255, 255, 0))
            rect = text.get_rect(center=(surface.get_width() // 2, 80))
            surface.blit(text, rect)
