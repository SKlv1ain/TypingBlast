import pygame as pg

class Dispatcher: 
    def __init__(self, parent):
        self.parent = parent 

    def __contains__(self, event_type):
        attrname = f'on_{pg.event.event_name(event_type).lower()}'
        return hasattr(self, attrname)

    def __getitem__(self, event_type):
        attrname = f'on_{pg.event.event_name(event_type).lower()}'
        return getattr(self, attrname)

class InputController(Dispatcher):
    def __init__(self, game_controller):
        super().__init__(None)
        self.game_controller = game_controller

    def on_keydown(self, event):
        if event.key == pg.K_ESCAPE:  # type: ignore
            pg.event.post(pg.event.Event(pg.QUIT))  # type: ignore
        else:
            self.game_controller.handle_input(event.unicode) 