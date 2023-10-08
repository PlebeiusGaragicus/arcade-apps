import time
from dataclasses import dataclass
from typing import Callable
import logging
logger = logging.getLogger()

import arcade

from gamelib.model.MenuAction import MenuAction
from gamelib.view.results_screen_template import ResultsViewTemplate
from snek.view.gameplay import GameplayView

from snek.app import GAME_WINDOW



class ResultsView( ResultsViewTemplate ):
    def __init__(self, gameplay_view: arcade.View):
        super().__init__()

        self.menu_actions.append( MenuAction("Revive ($)", self.revive) )
        self.menu_actions.append( MenuAction("Give up", self.main_menu) )

        self.gameplay_view: GameplayView = gameplay_view


    def revive(self):
        logger.info("reviving player...!")
        # self.gameplay_view.player.alive = True
        # self.gameplay_view.player.life = 100
        self.gameplay_view.revive()
        self.window.show_view(self.gameplay_view)

    def main_menu(self):
        from snek.view.menu import MenuView
        next_view = MenuView()
        self.window.show_view(next_view)


    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_BROWN)


    def on_update(self, delta_time):
        super().on_update(delta_time)


    def on_draw(self):
        arcade.start_render()

        arcade.draw_text("GAME OVER", GAME_WINDOW.width // 2, GAME_WINDOW.height * 0.8, arcade.color.RED, font_size=90, anchor_x="center", bold=True)

        x = GAME_WINDOW.width * 0.1
        y = GAME_WINDOW.height // 2
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