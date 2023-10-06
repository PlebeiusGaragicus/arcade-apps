import time
import logging
logger = logging.getLogger("game")

import arcade


class GameplayView(arcade.View):
    def __init__(self):
        super().__init__()
        self.start_time = time.time()
        self.last_life_loss = time.time()

        self.alive = True
        self.life = 100


    def on_show_view(self):
        logger.info("Starting gameplay view")
        arcade.set_background_color(arcade.color.BLACK_BEAN)


    def on_update(self, delta_time):
        if self.life <= 0 or self.alive is False:
            from template.views.menu import MenuView
            next_view = MenuView()
            self.window.show_view(next_view)
        
        # lose 1 life every 1 second
        if time.time() > self.last_life_loss + 1:
            self.life -= 1
            self.last_life_loss = time.time()
            logger.info("life: %s", self.life)


    def on_draw(self):
        arcade.start_render()

        # show life in top left corner
        arcade.draw_text(f"Life: {self.life}", 10, self.window.height * 0.9, arcade.color.WHITE, font_size=20, anchor_x="left")


    def on_key_press(self, symbol: int, modifiers: int):

        if symbol == arcade.key.ESCAPE:
            logger.info("escape")
            self.alive = False
            # arcade.exit()
