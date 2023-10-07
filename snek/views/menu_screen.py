import time
from dataclasses import dataclass
from typing import Callable
import logging
logger = logging.getLogger()

import arcade

from snek.config import AFK_TIMEOUT

@dataclass
class MenuAction:
    name: str
    action: Callable
    args: list = None
    kwargs: dict = None

    def execute(self):
        if self.args is None:
            self.args = []
        if self.kwargs is None:
            self.kwargs = {}
        self.action(*self.args, **self.kwargs)


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.last_input = time.time()
        self.selected_menu_item = 0

        self.menu_actions = [
            MenuAction("Start Game", self.start_game),
            # MenuAction("Options", arcade.close_window),
            MenuAction("Exit", arcade.close_window),
        ]


    def start_game(self):
        from snek.views.gameplay import GameplayView
        next_view = GameplayView()
        self.window.show_view(next_view)


    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_BROWN)


    def on_update(self, delta_time):
        # self-destruct in ten seconds if no input (user is AFK)
        if AFK_TIMEOUT > 0 and \
            time.time() > self.last_input + AFK_TIMEOUT:
                logger.warning("AFK timeout reached, exiting game - user is AFK!")
                arcade.exit()


    def on_draw(self):
        arcade.start_render()
        width, height = self.window.get_size()
        x = width * 0.1
        y = height // 2
        for i, menu_item in enumerate(self.menu_actions):
            if i == self.selected_menu_item:
                color = arcade.color.YELLOW
                arcade.draw_text(">", x - 30, y - i * 50, color, font_size=30, anchor_x="left")
            else:
                color = arcade.color.BLACK
            arcade.draw_text(menu_item.name, x, y - i * 50, color, font_size=30, anchor_x="left")


    def on_key_press(self, symbol: int, modifiers: int):
        self.last_input = time.time()

        if symbol == arcade.key.UP:
            if self.selected_menu_item > 0:
                self.selected_menu_item -= 1

        elif symbol == arcade.key.DOWN:
            if self.selected_menu_item < len(self.menu_actions) - 1:
                self.selected_menu_item += 1

        elif symbol == arcade.key.ENTER:
            logger.info("enter")
            # self.menu_actions[self.selected_menu_item].action()
            self.menu_actions[self.selected_menu_item].execute()

        elif symbol == arcade.key.ESCAPE:
            logger.info("escape")
            arcade.exit()
