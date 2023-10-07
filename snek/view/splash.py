import time
import logging
logger = logging.getLogger()

from gamelib.view.splash_screen_template import SplashScreenViewTemplate

from snek.app import GAME_WINDOW, MY_DIR

import arcade

class SplashScreenView(SplashScreenViewTemplate):
    def __init__(self, next_view: arcade.View, skip_intro: bool = False):
        super().__init__(next_view, MY_DIR, skip_intro)
        self.alpha = 0  # initialize alpha to 0 (fully transparent)


    def on_show_view(self):
        super().on_show_view()
        arcade.set_background_color(arcade.color.BLACK)




    def on_update(self, delta_time):
        #NOTE: you NEED to call super().on_update() in order to play the theme music!!!!
        super().on_update(delta_time)


    def on_draw(self):
        arcade.start_render()

        color_with_alpha = arcade.color.WHITE + (self.alpha,)  # create a color object with the desired alpha value
        arcade.draw_text("Loading a game...", GAME_WINDOW.width / 2, GAME_WINDOW.height / 2,
                         color_with_alpha,
                         font_size=30, anchor_x="center")
        self.alpha = min(self.alpha + 5, 255)  # increase alpha up to 255
