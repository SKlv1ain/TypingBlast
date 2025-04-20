from pathlib import Path
import pygame as pg

from Utils.config import ArgumentParser
from Utils.clock import Clock

from Views.screen import Screen
from Views.game_renderer import GameRenderer
from Views.menu import MenuView

from Controllers.menu_controller import MenuController
from Controllers.game_controller import GameController
from Controllers.input_controller import InputController

def run_game(screen, clock):
    # Setup Game MVC
    renderer = GameRenderer(screen)
    game_controller = GameController(renderer)
    input_controller = InputController(game_controller)

    # Game loop
    running = True
    while running:
        clock.tick()
        if pg.event.peek(pg.QUIT):
            return "quit"
        
        for event in pg.event.get():
            if event.type in input_controller:
                input_controller[event.type](event)

        game_controller.update()
        screen.clear()
        renderer.draw()
        screen.update() 
    return "menu"

def main(argv=None):
    parser = ArgumentParser(prog=Path(__file__).stem, description=main.__doc__)
    args = parser.parse_args(argv)

    pg.init()
    pg.mixer.init()


    clock = Clock(args.framerate)
    screen = Screen(args.size)

    game_state = "menu"
    menu_view = MenuView(screen)
    menu_controller = MenuController(menu_view)

    running = True
    while running:
        if game_state == "menu":
            menu_view.draw()
            game_state = menu_controller.handle_events()
        elif game_state == "start":
            game_state = run_game(screen, clock)
        elif game_state == "stats":
            print("Stats screen coming soon...")
            game_state = "menu"
        elif game_state == "quit":
            running = False

    pg.quit()

if __name__ == '__main__':
    main()
