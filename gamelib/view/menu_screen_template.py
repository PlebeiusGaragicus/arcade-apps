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
        # arcade.set_background_color(arcade.color.DARK_BROWN)


    def on_update(self, delta_time):
        raise NotImplementedError("on_update() must be implemented in child class")
        # # self-destruct in ten seconds if no input (user is AFK)
        # if AFK_TIMEOUT > 0 and \
        #     time.time() > self.last_input + AFK_TIMEOUT:
        #         logger.warning("AFK timeout reached, exiting game - user is AFK!")
        #         arcade.exit()


    def on_draw(self):
        raise NotImplementedError("on_draw() must be implemented in child class")
        # arcade.start_render()
        # width, height = self.window.get_size()
        # x = width * 0.1
        # y = height // 2
        # for i, menu_item in enumerate(self.menu_actions):
        #     if i == self.selected_menu_item:
        #         color = arcade.color.YELLOW
        #         arcade.draw_text(">", x - 30, y - i * 50, color, font_size=30, anchor_x="left")
        #     else:
        #         color = arcade.color.BLACK
        #     arcade.draw_text(menu_item.name, x, y - i * 50, color, font_size=30, anchor_x="left")


    def on_key_press(self, symbol: int, modifiers: int):
        raise NotImplementedError("on_key_press() must be implemented in child class")

        # self.last_input = time.time()

        # if symbol == arcade.key.UP:
        #     if self.selected_menu_item > 0:
        #         self.selected_menu_item -= 1

        # elif symbol == arcade.key.DOWN:
        #     if self.selected_menu_item < len(self.menu_actions) - 1:
        #         self.selected_menu_item += 1

        # elif symbol == arcade.key.ENTER:
        #     logger.info("enter")
        #     # self.menu_actions[self.selected_menu_item].action()
        #     self.menu_actions[self.selected_menu_item].execute()

        # elif symbol == arcade.key.ESCAPE:
        #     logger.info("escape")
        #     arcade.exit()

    def is_user_afk(self) -> bool:
        # self-destruct in ten seconds if no input (user is AFK)
        if self.afk_timeout > 0 and \
            time.time() > self.last_input + self.afk_timeout:
                logger.warning("AFK timeout reached, exiting game - user is AFK!")
                return True

    def reset_afk_timer(self):
        self.last_input = time.time()
