# views/dashboard_view.py
import pygame as pg

class DashboardView:
    def __init__(self, screen):
        self.screen = screen
        self.font = pg.font.Font(None, 16)
        self.color = (200, 200, 200) # Light gray
        self.bg_color = (30, 30, 45)  # Dark gray
        self.padding = 10 # 
        self.line_spacing = 28  
        self.position = (20,420) # Top-left corner of the screen

    def draw(self, stats):
        lines = [
            f"WPM: {stats.get('WPM', 0):.2f}",
            f"Accuracy (%): {stats.get('Accuracy (%)', 0):.1f}",
            f"Words Destroyed: {stats.get('Words Destroyed', 0)}",
            f"Max Combo: {stats.get('Max Combo', 0)}",
            f"Score: {stats.get('Score', 0)}",
            f"Typing Errors: {stats.get('Typing Errors', 0)}",
            f"Wave: {stats.get('Wave', 0)}",
        ]

        x, y = self.position
        
        for i, line in enumerate(lines):
            text = self.font.render(line, True, self.color)
            self.screen.image.blit(text, (x, y + i * self.line_spacing))
