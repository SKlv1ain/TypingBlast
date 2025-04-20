import pygame as pg

class MenuController:
    def __init__(self, menu_view):
        self.menu_view = menu_view

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return "quit"
            elif event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                for name, rect in self.menu_view.buttons.items():
                    if rect.collidepoint(pos):
                        return name.lower()  # "start", "stats", "quit"
        return "menu"


