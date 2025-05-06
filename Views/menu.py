# import pygame as pg

# class MenuView:
#     def __init__(self, screen):
#         self.screen = screen.image
#         self.font = pg.font.Font(None, 64)
#         self.button_font = pg.font.Font(None, 48)

#         self.buttons = {
#             "Start": pg.Rect(300, 250, 200, 60),
#             "Stats": pg.Rect(300, 330, 200, 60),
#             "Quit": pg.Rect(300, 410, 200, 60)
#         }

#     def draw(self):
#         self.screen.fill((20, 20, 30))
#         title = self.font.render("Typing Blast: Space Shooter", True, (255, 255, 255))
#         self.screen.blit(title, (160, 120))

#         for text, rect in self.buttons.items():
#             pg.draw.rect(self.screen, (70, 70, 200), rect, border_radius=8)
#             label = self.button_font.render(text, True, (255, 255, 255))
#             label_rect = label.get_rect(center=rect.center)
#             self.screen.blit(label, label_rect)

#         pg.display.flip()


import pygame as pg
import random

class MenuView:
    def __init__(self, screen):
        self.screen = screen.image
        self.screen_rect = self.screen.get_rect()
        self.font = pg.font.Font(None, 96)
        self.button_font = pg.font.Font(None, 48)

        # Starfield setup
        self.stars = [(random.randint(0, self.screen_rect.width), 
                       random.randint(0, self.screen_rect.height)) for _ in range(100)] 

        # Define buttons
        button_width = 260
        button_height = 70
        spacing = 50
        center_x = self.screen_rect.centerx

        self.button_data = ["Start", "Stats", "Quit"]
        self.buttons = []
        title_bottom_y = 200  # Adjust as needed depending on your title size
        start_y = title_bottom_y + 60  # start buttons lower with padding


        for i, text in enumerate(self.button_data):
            rect = pg.Rect(0, 0, button_width, button_height)
            rect.center = (center_x, start_y + i * (button_height + spacing))
            self.buttons.append((text, rect))

    def draw_starfield(self):
        for i, (x, y) in enumerate(self.stars):
            pg.draw.circle(self.screen, (200, 200, 255), (x, y), 1)
            y += 1  # constant speed
            if y > self.screen_rect.height:
                y = 0
            self.stars[i] = (x, y)


    def draw(self):
        # Background with starfield
        self.screen.fill((10, 10, 25))
        self.draw_starfield()

        # Game title with neon glow
        title_surf = self.font.render("Typing Blast", True, (255, 255, 255))
        glow = self.font.render("Typing Blast", True, (100, 100, 255))
        title_rect = title_surf.get_rect(center=(self.screen_rect.centerx, 100))
        glow_rect = glow.get_rect(center=(self.screen_rect.centerx + 2, 102))
        self.screen.blit(glow, glow_rect)
        self.screen.blit(title_surf, title_rect)

        # Buttons
        for text, rect in self.buttons:
            mouse_pos = pg.mouse.get_pos()
            is_hovered = rect.collidepoint(mouse_pos)
            alpha = 200 if is_hovered else 120
            base_color = (80, 120, 255) if is_hovered else (50, 60, 100)

            # Glass effect
            button_surf = pg.Surface((rect.width, rect.height), pg.SRCALPHA)
            button_surf.fill((base_color[0], base_color[1], base_color[2], alpha))
            pg.draw.rect(button_surf, (255, 255, 255, 40), button_surf.get_rect(), width=2, border_radius=12)
            self.screen.blit(button_surf, rect.topleft)

            # Button text
            label = self.button_font.render(text, True, (255, 255, 255))
            label_rect = label.get_rect(center=rect.center)
            self.screen.blit(label, label_rect)

        pg.display.flip()
