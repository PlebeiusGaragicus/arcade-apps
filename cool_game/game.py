import logging
logger = logging.getLogger("game")

import arcade



class Singleton:
    _instance = None

    def __init__(self):
        raise Exception("Cannot directly instantiate a Singleton. Access via get_instance()")

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
        return cls._instance




FULLSCREEN = True
SCREEN_TITLE = "testing a game"

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


        width, height = arcade.get_display_size()

        width //= 2
        height //= 2

        if FULLSCREEN:
            game.window = arcade.Window(title=SCREEN_TITLE, fullscreen=True)
        else:
            game.window = arcade.Window(width=width, height=height, title=SCREEN_TITLE)

        game.window.set_mouse_visible(False)

        return cls._instance


    def start(self):
        logger.info("game::start()")

        from cool_game.splash_screen import SplashScreen
        view = SplashScreen()
        self.window.show_view(view)

        arcade.run()
