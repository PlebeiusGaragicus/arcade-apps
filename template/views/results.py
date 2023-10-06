import time
from dataclasses import dataclass
from typing import Callable
import logging
logger = logging.getLogger()

import arcade

from template.config import AFK_TIMEOUT

@dataclass
class MenuAction:
    name: str
    action: Callable
    args: list = None
    kwargs: dict = None


class ResultsView(arcade.View):
    def __init__(self, gameplay_view: arcade.View):
        super().__init__()
        self.last_input = time.time()
        self.menu_actions = [
            MenuAction("CONTINUE      -   never give up!", self.revive),
            MenuAction("QUIT          -   accept your fate...", self.main_menu),
        ]
        self.selected_menu_item = 0

        self.gameplay_view = gameplay_view


    def revive(self):
        logger.debug("reviving player...!")
        self.gameplay_view.alive = True
        self.gameplay_view.life = 100
        self.window.show_view(self.gameplay_view)

    def main_menu(self):
        from template.views.menu import MenuView
        next_view = MenuView()
        self.window.show_view(next_view)


    def on_show_view(self):
        logger.info("Starting gameplay view")
        arcade.set_background_color(arcade.color.DARK_BROWN)


    def on_update(self, delta_time):
        if time.time() > self.last_input + AFK_TIMEOUT: # self-destruct in ten seconds if no input (user is AFK)
            logger.warning("AFK timeout reached, exiting game - user is AFK!")
            self.main_menu()


    def on_draw(self):
        arcade.start_render()
        width, height = self.window.get_size()

        arcade.draw_text("GAME OVER", width // 2, height * 0.8, arcade.color.RED, font_size=90, anchor_x="center", bold=True)

        x = width * 0.1
        y = height // 2
        for i, menu_item in enumerate(self.menu_actions):
            if i == self.selected_menu_item:
                color = arcade.color.YELLOW
                arcade.draw_text(">", x - 30, y - i * 50, color, font_size=30, anchor_x="left")
            else:
                color = arcade.color.BLACK
            # TODO - go for a monospaced font here
            arcade.draw_text(menu_item.name, x, y - i * 50, color, font_size=30, anchor_x="left", font_name="/Users/myca/arcade-apps/template/resources/Andale Mono.ttf")


    def on_key_press(self, symbol: int, modifiers: int):
        self.last_input = time.time()

        if symbol == arcade.key.UP:
            if self.selected_menu_item > 0:
                self.selected_menu_item -= 1
        elif symbol == arcade.key.DOWN:
            if self.selected_menu_item < len(self.menu_actions) - 1:
                self.selected_menu_item += 1

        elif symbol == arcade.key.ENTER:
            self.menu_actions[self.selected_menu_item].action()

        elif symbol == arcade.key.ESCAPE:
            self.main_menu()
