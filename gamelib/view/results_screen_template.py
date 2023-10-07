import time
import logging
logger = logging.getLogger()

import arcade


class ResultsViewTemplate(arcade.View):
    def __init__(self, afk_timeout: int | None = None):
        super().__init__()
        self.afk_timeout = afk_timeout # if None, then no timeout
        self.last_input = time.time()

        self.menu_actions = []
        self.selected_menu_item = 0


    def on_show_view(self):
        raise Exception("on_show_view() not implemented - you need to implement this in your subclass!")


    def on_update(self, delta_time):
        if self.afk_timeout is not None:    
            if time.time() > self.last_input + self.afk_timeout: # self-destruct in ten seconds if no input (user is AFK)
                logger.warning("AFK timeout reached, exiting game - user is AFK!")
                self.main_menu()


    def on_draw(self):
        raise Exception("on_draw() not implemented - you need to implement this in your subclass!")

    def on_key_press(self, symbol: int, modifiers: int):
        raise Exception("on_key_press() not implemented - you need to implement this in your subclass!")