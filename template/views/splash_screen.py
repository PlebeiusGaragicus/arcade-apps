import time
import logging
logger = logging.getLogger()

from template.game import Game

import arcade

# for type hinting
from pyglet.media import Player

SPLASH_SCREEN_TIME_DELAY = 2

class SplashScreenView(arcade.View):
    def __init__(self):
        super().__init__()
        self.alpha = 0  # initialize alpha to 0 (fully transparent)
        self.player: Player = None
        self.theme_len = 0

    
    def on_show_view(self):
        logger.info("Starting SplashScreen")
        arcade.set_background_color(arcade.color.BLACK)
        self.start_time = time.time()


    def on_update(self, delta_time):
        if time.time() > self.start_time + SPLASH_SCREEN_TIME_DELAY or Game.get_instance().manifest.get('skip_intro', False):
            from template.views.menu import MenuView
            next_view = MenuView()
            self.window.show_view(next_view)


    def on_draw(self):
        width, height = self.window.get_size()

        arcade.start_render()

        color_with_alpha = arcade.color.WHITE + (self.alpha,)  # create a color object with the desired alpha value
        arcade.draw_text("Loading a game...", width / 2, height / 2,
                         color_with_alpha,
                         font_size=30, anchor_x="center")
        self.alpha = min(self.alpha + 5, 255)  # increase alpha up to 255
