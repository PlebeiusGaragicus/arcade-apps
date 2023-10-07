import os
import json
import logging
logger = logging.getLogger()

import arcade

from snek.logger import setup_logging

GAME_WINDOW: arcade.Window = None


class Singleton:
    _instance = None
    def __init__(self):
        raise Exception("Cannot directly instantiate a Singleton. Access via get_instance()")
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
        return cls._instance


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

        if self.manifest.get('skip_intro', False):
            from snek.views.menu_screen import MenuView
            view = MenuView()
            self.window.show_view(view)
        else:
            from snek.views.splash_screen import SplashScreenView
            view = SplashScreenView()
            self.window.show_view(view)

        arcade.run()
