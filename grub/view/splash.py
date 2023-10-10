import os
import time
import logging
logger = logging.getLogger()

import arcade

# for type hinting
from pyglet.media import Player


from grub.app import GAME_WINDOW, MY_DIR


class SplashScreenView( arcade.View ):



    def __init__(self, next_view: arcade.View, skip_intro: bool = False):
        super().__init__()
        self.next_view: arcade.View = next_view
        self.music_player: Player = None
        self.start_time = time.time()
        self.skip_intro = skip_intro

        self.alpha = 0  # initialize alpha to 0 (fully transparent)

        sound_path = os.path.join(MY_DIR, 'resources', 'sounds', 'intro.wav')

        self.theme_sound = arcade.sound.load_sound( sound_path )
        self.theme_len = arcade.sound.Sound.get_length( self.theme_sound )


    def on_show_view(self):
        super().on_show_view()
        arcade.set_background_color(arcade.color.BLACK)
        self.player = arcade.sound.play_sound( self.theme_sound )




    def on_update(self, delta_time):
        if time.time() > self.start_time + self.theme_len or self.skip_intro: # wait for theme to finish
            arcade.sound.stop_sound( self.player )
            self.window.show_view(self.next_view)



    def on_draw(self):
        arcade.start_render()

        color_with_alpha = arcade.color.AIR_FORCE_BLUE + (self.alpha,)  # create a color object with the desired alpha value
        arcade.draw_text("Loading a game...", GAME_WINDOW.width / 2, GAME_WINDOW.height / 2,
                         color_with_alpha,
                         font_size=30, anchor_x="center")
        self.alpha = min(self.alpha + 5, 255)  # increase alpha up to 255
