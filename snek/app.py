import os
import json
import logging
logger = logging.getLogger()

import pygame

from gamelib.logger import setup_logging
from gamelib.singleton import Singleton

from snek.gamestate import GameStateManager
from snek.config import *




class App(Singleton):
    manifest: dict = None
    manager: GameStateManager = None


    @classmethod
    def get_instance(cls):
        if cls._instance:
            return cls._instance
        else:
            return cls.configure_instance()

    @classmethod
    def configure_instance(cls):
        if cls._instance:
            raise Exception("Instance already configured")
        application = cls.__new__(cls)
        cls._instance = application

        setup_logging()

        # load manifest
        manifest_path = os.path.join( os.path.dirname(os.path.abspath(__file__)), 'manifest.json' )
        with open( manifest_path ) as f:
            application.manifest = json.load(f)

        #### setup application variables! ####
        pygame.init()
        pygame.display.set_caption("Snake Game")
        application.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        application.clock = pygame.time.Clock()
        application.manager = GameStateManager()

        from snek.views.mainmenu import MainMenu
        from snek.views.gameplay import Gameplay
        from snek.views.gameover import GameOver
        application.manager.add_state("main_menu", MainMenu())
        application.manager.add_state("gameplay", Gameplay())
        application.manager.add_state("game_over", GameOver())

        application.window_title = application.manifest['name']
        logger.debug("manifest: %s", application.manifest)

        # display_width, display_height = arcade.get_display_size()


        # TODO - consider making all windows resizable in order to test layout for multiple monitors
        # game.window = arcade.Window(width=display_width, height=display_height, title=window_title, fullscreen=False, style="borderless")
        # game.window.set_mouse_visible(False)

        return cls._instance


    def start(self):
        # global GAME_WINDOW
        # GAME_WINDOW = self.window

        self.manager.change_state("main_menu")

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.manager.handle_event(event)

            self.manager.update()
            self.manager.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

        # try:
        #     arcade.run()
        # except Exception as e:
        #     # TODO - do something useful and cool here.. make my own exception view like the seedsigner!
        #     logger.exception(e)
        #     raise e
