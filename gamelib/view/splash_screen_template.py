import os
import time
import logging
logger = logging.getLogger()


import arcade

# for type hinting
from pyglet.media import Player

class SplashScreenViewTemplate(arcade.View):
    def __init__(self, next_view: arcade.View, game_directory: str, skip_intro: bool = False):
        super().__init__()
        self.next_view: arcade.View = next_view
        self.music_player: Player = None
        self.start_time = time.time()

        sound_path = os.path.join(game_directory, 'resources', 'sounds', 'intro.wav')

        self.theme_sound = arcade.sound.load_sound( sound_path )
        self.theme_len = arcade.sound.Sound.get_length( self.theme_sound )


    def on_show_view(self):
        self.player = arcade.sound.play_sound( self.theme_sound )

        # raise NotImplementedError("on_show_view() not implemented - you need to implement this in your subclass!")


    def on_update(self, delta_time):
        if time.time() > self.start_time + self.theme_len: # wait for theme to finish
            arcade.sound.stop_sound( self.player )
            self.window.show_view(self.next_view)
        # raise NotImplementedError("on_update() not implemented - you need to implement this in your subclass!")


    def on_draw(self):
        raise NotImplementedError("on_draw() not implemented - you need to implement this in your subclass!")