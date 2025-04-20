import pygame as pg

class MenuView:
    def __init__(self, screen):
        self.screen = screen.image
        self.font = pg.font.Font(None, 64)
        self.button_font = pg.font.Font(None, 48)

        self.buttons = {
            "Start": pg.Rect(300, 250, 200, 60),
            "Stats": pg.Rect(300, 330, 200, 60),
            "Quit": pg.Rect(300, 410, 200, 60)
        }

    def draw(self):
        self.screen.fill((20, 20, 30))
        title = self.font.render("Typing Blast: Space Shooter", True, (255, 255, 255))
        self.screen.blit(title, (160, 120))

        for text, rect in self.buttons.items():
            pg.draw.rect(self.screen, (70, 70, 200), rect, border_radius=8)
            label = self.button_font.render(text, True, (255, 255, 255))
            label_rect = label.get_rect(center=rect.center)
            self.screen.blit(label, label_rect)

        pg.display.flip()
