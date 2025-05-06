from Controllers.menu_controller import MenuController
from Controllers.game_controller import GameController
from Controllers.input_controller import InputController


from Views.menu import MenuView
from Views.game_renderer import GameRenderer
from Views.gameover_view import GameOverView


import pygame as pg

from Utils.save_to_csv import save_to_csv

class StateController:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.state = "menu"

    def run(self):
        while True:
            if self.state == "menu":
                self.state = self.run_menu()
            elif self.state == "start":
                self.state = self.run_game()
            elif self.state == "stats":
                print("Stats coming soon...")
                self.state = "menu"
            elif self.state == "quit":
                break
            else:
                print(f"Unknown state: {self.state}")
                break

    def run_menu(self):
        menu_view = MenuView(self.screen)
        menu_controller = MenuController(menu_view)
        while True:
            menu_view.draw()
            action = menu_controller.handle_events()
            if action in ("start", "quit", "stats"):
                return action

    def run_game(self):
        renderer = GameRenderer(self.screen)
        game_controller = GameController(renderer)
        input_controller = InputController(game_controller)

        while not game_controller.is_over():
            self.clock.tick()
            if pg.event.peek(pg.QUIT):
                break

            for event in pg.event.get():
                if event.type in input_controller:
                    input_controller[event.type](event)

            game_controller.update()
            self.screen.clear()
            renderer.draw()
            
            game_controller.dashboard.draw(game_controller.stats.export())
            
            self.screen.update()

        final_stats = game_controller.get_final_stats()
        save_to_csv(final_stats)
        # for k, v in final_stats.items():
        #     print(f"{k}: {v}")
        return GameOverView(self.screen).show(final_stats)

        
    def run_stats(self):
        ...

      

