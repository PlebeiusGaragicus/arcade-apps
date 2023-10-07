import os
import json
import logging
logger = logging.getLogger()

import arcade

from gamelib.logger import setup_logging
from gamelib.model.singleton import Singleton

MY_DIR = os.path.dirname(os.path.abspath(__file__))
GAME_WINDOW: arcade.Window = None





class Game(Singleton):
    window: arcade.Window = None
    manifest: dict = None

    @classmethod
    def get_instance(cls):
        if cls._instance:
            return cls._instance
        else:
            return cls.configure_instance()

    @classmethod
    def configure_instance(cls, disable_hardware=False):
        if cls._instance:
            raise Exception("Instance already configured")
        game = cls.__new__(cls)
        cls._instance = game

        setup_logging()

        # load manifest
        manifest_path = os.path.join( os.path.dirname(os.path.abspath(__file__)), 'manifest.json' )
        with open( manifest_path ) as f:
            game.manifest = json.load(f)

        logger.debug("manifest: %s", game.manifest)

        display_width, display_height = arcade.get_display_size()

        window_title = game.manifest['name']

        # TODO - consider making all windows resizable in order to test layout for multiple monitors
        game.window = arcade.Window(width=display_width, height=display_height, title=window_title, fullscreen=False, style="borderless")

        game.window.set_mouse_visible(False)

        return cls._instance


    def start(self):
        logger.info("start()")

        global GAME_WINDOW
        GAME_WINDOW = self.window


        from snek.view.splash import SplashScreenView
        from snek.view.menu import MenuView

        view = SplashScreenView( MenuView() )
        self.window.show_view(view)

        # if self.manifest.get('skip_intro', False):
        #     from snek.view.menu_screen import MenuView
        #     view = MenuView(self)
        #     self.window.show_view(view)
        # else:

        try:
            arcade.run()
        except Exception as e:
            # TODO - do something useful and cool here.. make my own exception view like the seedsigner!
            logger.exception(e)
            raise e

    def start_gameplay(self):
        from snek.view.gameplay import GameplayView
        view = GameplayView()
        self.window.show_view(view)
