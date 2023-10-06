import time
import math
import logging
logger = logging.getLogger()

import arcade


HOLD_TO_QUIT_SECONDS = 3


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arcade.make_soft_square_texture(50, arcade.color.RED, outer_alpha=255)
        self.center_x = 100
        self.center_y = 100

    def update(self):
        self.center_x += 1
        self.center_y += 1


class GameplayView(arcade.View):
    def __init__(self):
        super().__init__()
        self.start_time = time.time()
        self.last_life_loss = time.time()

        self.alive = True
        self.life = 100

        self.player = Player()

        self.paused = False
        self.escape_pressed_time = None


    def on_show_view(self):
        logger.info("Starting gameplay view")
        arcade.set_background_color(arcade.color.BLACK_BEAN)


    def on_update(self, delta_time):
        if self.life <= 0 or self.alive is False:
            from template.views.menu import MenuView
            next_view = MenuView()
            self.window.show_view(next_view)

        if self.paused:
            return

        # lose 1 life every 1 second
        if time.time() > self.last_life_loss + 1:
            self.life -= 1
            self.last_life_loss = time.time()
            logger.info("life: %s", self.life)

        self.player.update()

        # if self.escape_pressed_time is not None:
        #     time_elapsed = time.time() - self.escape_pressed_time
        #     if time_elapsed >= HOLD_TO_QUIT_SECONDS:
        #         self.alive = False
        #         self.escape_pressed_time = None
        #     else:
        #         self.draw_timer_wheel(time_elapsed)


    def on_draw(self):
        arcade.start_render()

        # show life in top left corner
        arcade.draw_text(f"Life: {self.life}", 10, self.window.height * 0.9, arcade.color.WHITE, font_size=20, anchor_x="left")

        # draw player
        self.player.draw()

        if self.paused:
            # draw pause screen
            arcade.draw_rectangle_filled(self.window.width / 2, self.window.height / 2, self.window.width, self.window.height, arcade.color.BLACK_OLIVE + (200,))
            arcade.draw_text("PAUSED", self.window.width / 2, self.window.height * 0.75, arcade.color.YELLOW_ROSE, font_size=60, anchor_x="center", anchor_y="center")

        if self.escape_pressed_time is not None:
            time_elapsed = time.time() - self.escape_pressed_time
            if time_elapsed >= HOLD_TO_QUIT_SECONDS:
                self.alive = False
                self.escape_pressed_time = None
            else:
                self.draw_timer_wheel(time_elapsed)



    def on_key_press(self, symbol: int, modifiers: int):

        if symbol == arcade.key.ESCAPE:
            logger.info("escape")
            self.escape_pressed_time = time.time()
            self.paused = True

        elif symbol == arcade.key.P:
            logger.info("pause")
            self.paused = not self.paused

    
    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            logger.info("escape released")
            self.escape_pressed_time = None
            self.paused = False


    def draw_timer_wheel(self, time_elapsed):
        center_x = self.window.width // 2
        center_y = self.window.height * 0.5
        radius = 100

        start_angle = 360
        end_angle = 360 - ((HOLD_TO_QUIT_SECONDS - time_elapsed) / HOLD_TO_QUIT_SECONDS) * 360
        # print(f"start_angle: {start_angle}" + "  " + f"end_angle: {end_angle}")

        # TODO: twine between colors as time elapses
        arcade.draw_arc_filled(center_x, center_y, radius, radius, arcade.color.WHITE, end_angle, start_angle, 90)
        arcade.draw_text(f"Hold <ESCAPE> to quit", center_x, center_y - radius, arcade.color.WHITE_SMOKE, font_size=20, anchor_x="center", anchor_y="center")
