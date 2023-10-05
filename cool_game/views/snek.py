import time
import logging
logger = logging.getLogger("lnarcade")

import arcade


class SnekView(arcade.View):
    def __init__(self):
        super().__init__()
        self.start_time = time.time()

    
    def on_show_view(self):
        logger.info("Starting gameplay view")
        arcade.set_background_color(arcade.color.BLUE)


    def on_update(self, delta_time):
        if time.time() > self.start_time + 5: # self-destruct in ten seconds
            arcade.exit()


    def on_draw(self):
        width, height = self.window.get_size()
        arcade.start_render()



    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.UP:
            logger.info("up")
        elif symbol == arcade.key.DOWN:
            logger.info("down")
        elif symbol == arcade.key.ENTER:
            logger.info("enter")
        elif symbol == arcade.key.ESCAPE:
            logger.info("escape")
            arcade.exit()
