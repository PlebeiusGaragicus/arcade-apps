import time
import logging
logger = logging.getLogger()

import arcade

from gamelib.model.MenuAction import MenuAction
from gamelib.view.menu_screen_template import MenuViewTemplate

from snek.config import AFK_TIMEOUT
from snek.app import GAME_WINDOW


class MenuView(MenuViewTemplate):
    def __init__(self):
        super().__init__( AFK_TIMEOUT )
        self.selected_menu_item = 0

        self.menu_actions.append( MenuAction("Start Game", self.start_game) )
        self.menu_actions.append( MenuAction("Exit", arcade.close_window) )



    def start_game(self):
        from snek.view.gameplay import GameplayView
        next_view = GameplayView()
        self.window.show_view(next_view)



    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_BROWN)



    def on_update(self, delta_time):
        if super().is_user_afk():
            arcade.exit() # TODO - maybe show a "you're afk" screen instead of just exiting the game? (like a screensaver or sample gameplay)



    def on_draw(self):
        arcade.start_render()
        x = GAME_WINDOW.width * 0.1
        y = GAME_WINDOW.height // 2
        for i, menu_item in enumerate(self.menu_actions):
            if i == self.selected_menu_item:
                color = arcade.color.YELLOW
                arcade.draw_text(">", x - 30, y - i * 50, color, font_size=30, anchor_x="left")
            else:
                color = arcade.color.BLACK
            arcade.draw_text(menu_item.name, x, y - i * 50, color, font_size=30, anchor_x="left")


    def on_key_press(self, symbol: int, modifiers: int):
        super().reset_afk_timer()

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
