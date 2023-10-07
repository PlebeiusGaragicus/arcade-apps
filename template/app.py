import os
import json
import logging
logger = logging.getLogger()

import arcade

from template.logger import setup_logging
from template import config



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

        # game.width, game.height = arcade.get_display_size()
        config.WINDOW_WIDTH, config.WINDOW_HEIGHT = arcade.get_display_size()


        window_title = game.manifest['name']

        # TODO - consider making all windows resizable in order to test layout for multiple monitors
        # game.window = arcade.Window(width=game.width, height=game.height, title=window_title, fullscreen=False, style="borderless")
        game.window = arcade.Window(width=config.WINDOW_WIDTH, height=config.WINDOW_HEIGHT, title=window_title, fullscreen=False, style="borderless")
        game.window.set_mouse_visible(False)

        return cls._instance


    def start(self):
        logger.info("start()")

        from template.views.splash_screen import SplashScreenView
        view = SplashScreenView()
        self.window.show_view(view)

        arcade.run()
