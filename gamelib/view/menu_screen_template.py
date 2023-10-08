import time
from dataclasses import dataclass
from typing import Callable
import logging
logger = logging.getLogger()

import arcade

from gamelib.model.singleton import Singleton
from gamelib.model.MenuAction import MenuAction


class MenuViewTemplate(arcade.View):
    def __init__(self, afk_timeout: int = 0):
        super().__init__()
        self.last_input = time.time()
        self.afk_timeout = afk_timeout
        self.menu_actions = []


    def on_show_view(self):
        raise NotImplementedError("on_show_view() must be implemented in child class")


    def on_update(self, delta_time):
        raise NotImplementedError("on_update() must be implemented in child class")


    def on_draw(self):
        raise NotImplementedError("on_draw() must be implemented in child class")


    def on_key_press(self, symbol: int, modifiers: int):
        raise NotImplementedError("on_key_press() must be implemented in child class")


    def is_user_afk(self) -> bool:
        # self-destruct in ten seconds if no input (user is AFK)
        if self.afk_timeout > 0 and \
            time.time() > self.last_input + self.afk_timeout:
                logger.warning("AFK timeout reached, exiting game - user is AFK!")
                return True

    def reset_afk_timer(self):
        self.last_input = time.time()
