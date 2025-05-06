# views/game_over_view.py
import pygame as pg

class GameOverView:
    def __init__(self, screen):
        self.screen = screen
        self.title_font = pg.font.Font(None, 72)
        self.label_font = pg.font.Font(None, 36)
        self.value_font = pg.font.Font(None, 36)
        self.button_font = pg.font.Font(None, 36)
        self.back_button = pg.Rect(280, 460, 240, 60)

    def draw(self, stats):
        self.screen.clear()
        self.screen.image.fill((20, 20, 30))

        # Draw centered title with shadow
        title_text = self.title_font.render("Game Over", True, (255, 100, 100))
        shadow = self.title_font.render("Game Over", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(self.screen.image.get_width() // 2, 100))
        shadow_rect = shadow.get_rect(center=(self.screen.image.get_width() // 2 + 1, 101))
        self.screen.image.blit(shadow, shadow_rect)
        self.screen.image.blit(title_text, title_rect)

        # Draw stat box
        box_rect = pg.Rect(150, 180, 500, 250)
        pg.draw.rect(self.screen.image, (40, 40, 60), box_rect, border_radius=12)
        pg.draw.rect(self.screen.image, (100, 100, 255), box_rect, 2, border_radius=12)

        for i, (k, v) in enumerate(stats.items()):
            label = self.label_font.render(f"{k}:", True, (200, 200, 200))
            value = self.value_font.render(str(v), True, (255, 255, 255))
            y = 200 + i * 35
            self.screen.image.blit(label, (180, y))
            self.screen.image.blit(value, (420, y))

        # Back button
        pg.draw.rect(self.screen.image, (100, 100, 250), self.back_button, border_radius=8)
        pg.draw.rect(self.screen.image, (255, 255, 255), self.back_button, 2, border_radius=8)
        btn_text = self.button_font.render("Back to Menu", True, (255, 255, 255))
        btn_rect = btn_text.get_rect(center=self.back_button.center)
        self.screen.image.blit(btn_text, btn_rect)

        self.screen.update()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return "quit"
            elif event.type == pg.MOUSEBUTTONDOWN:
                if self.back_button.collidepoint(pg.mouse.get_pos()):
                    return "menu"
        return None

    def show(self, stats):
        while True:
            self.draw(stats)
            action = self.handle_events()
            if action:
                return action