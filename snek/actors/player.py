import time
import logging
logger = logging.getLogger()

import arcade

from snek.app import GAME_WINDOW

# NOTE: only for MacOS... need to test on rpi
# this is because of the menu bar / camera cutout on the macbook air
TOP_BAR_HEIGHT = 30


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.size = 50
        self.texture = arcade.make_soft_square_texture(self.size, arcade.color.RED, center_alpha=255, outer_alpha=55)

        self.center_x = 100
        self.center_y = 100
        self.dir_x = 1
        self.dir_y = 1

        self.life = 100
        self.last_life_loss = time.time()


    def update(self):
        # lose life every second
        if time.time() > self.last_life_loss + 1:
            self.life -= 5
            self.last_life_loss = time.time()
            # logger.info("life: %s", self.life)

        self.center_x += self.dir_x
        self.center_y += self.dir_y

        if self.center_x > GAME_WINDOW.width - self.size // 2:
            self.dir_x = -self.dir_x
        elif self.center_x < 0 + self.size // 2:
            self.dir_x = -self.dir_x

        if self.center_y > GAME_WINDOW.height - self.size // 2 - TOP_BAR_HEIGHT:
            self.dir_y = -self.dir_y
        elif self.center_y < 0 + self.size // 2:
            self.dir_y = -self.dir_y
