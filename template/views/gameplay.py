import time
import math
import logging
logger = logging.getLogger()

import arcade


HOLD_TO_QUIT_SECONDS = 1.5

TOP_BAR_HEIGHT = 30

# move to config.py ???
window_width, window_height = arcade.get_display_size()







class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.size = 50
        self.texture = arcade.make_soft_square_texture(self.size, arcade.color.RED, center_alpha=255, outer_alpha=55)
        self.center_x = 100
        self.center_y = 100

        self.dir_x = 1
        self.dir_y = 1

    def update(self):
        self.center_x += self.dir_x
        self.center_y += self.dir_y

        if self.center_x > window_width - self.size // 2:
            self.dir_x = -self.dir_x
        elif self.center_x < 0 + self.size // 2:
            self.dir_x = -self.dir_x

        if self.center_y > window_height - self.size // 2 - TOP_BAR_HEIGHT:
            self.dir_y = -self.dir_y
        elif self.center_y < 0 + self.size // 2:
            self.dir_y = -self.dir_y



class CooldownKey():
    def __init__(self, symbol, cooldown_seconds):
        self.symbol = symbol
        self.cooldown_seconds = cooldown_seconds
        self.pressed = False
        self.last_pressed_time = None

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == self.symbol:
            if self.last_pressed_time is None or time.time() > self.last_pressed_time + self.cooldown_seconds:
                self.last_pressed_time = time.time()
                self.pressed = True
                return True
            else:
                print(f"cooldown for {self.symbol} not ready yet. {time.time() - self.last_pressed_time}")
                self.pressed = True
                return False
        else:
            return False

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == self.symbol:
            self.pressed = False
            return True
        else:
            return False

    def update_if_pressed(self):
        if self.pressed is True:
            if self.last_pressed_time is None or time.time() > self.last_pressed_time + self.cooldown_seconds:
                self.last_pressed_time = time.time()
                return True
            else:
                print(f"cooldown for {self.symbol} not ready yet. {time.time() - self.last_pressed_time}")
                return False


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

        self.cooldown_left = CooldownKey(arcade.key.LEFT, 0.1)
        self.cooldown_right = CooldownKey(arcade.key.RIGHT, 0.1)
        self.cooldown_up = CooldownKey(arcade.key.UP, 0.1)
        self.cooldown_down = CooldownKey(arcade.key.DOWN, 0.1)



    def on_show_view(self):
        logger.info("Starting gameplay view")
        arcade.set_background_color(arcade.color.BLACK_BEAN)


    def on_update(self, delta_time):
        if self.life <= 0 or self.alive is False:
            from template.views.results import ResultsView
            next_view = ResultsView(self)
            self.window.show_view(next_view)

        if self.paused:
            return

        # lose life every second
        if time.time() > self.last_life_loss + 1:
            self.life -= 5
            self.last_life_loss = time.time()
            logger.info("life: %s", self.life)

        self.player.update()

        if self.cooldown_up.update_if_pressed():
            self.player.dir_y += 1
        if self.cooldown_down.update_if_pressed():
            self.player.dir_y += -1
        if self.cooldown_left.update_if_pressed():
            self.player.dir_x += -1
        if self.cooldown_right.update_if_pressed():
            self.player.dir_x += 1





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
        
        if self.paused:
            return

        elif symbol == arcade.key.SPACE:
            logger.info("space")
            self.life += 10


        # these can't be elif!
        if self.cooldown_up.on_key_press(symbol, modifiers):
            logger.info("up")
            self.player.dir_y += 1
        if self.cooldown_down.on_key_press(symbol, modifiers):
            logger.info("down")
            self.player.dir_y += -1
        if self.cooldown_left.on_key_press(symbol, modifiers):
            logger.info("left")
            self.player.dir_x += -1
        if self.cooldown_right.on_key_press(symbol, modifiers):
            logger.info("right")
            self.player.dir_x += 1

    
    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            logger.info("escape released")
            self.escape_pressed_time = None
            self.paused = False
        
        if self.paused:
            return
        
        self.cooldown_up.on_key_release(symbol, modifiers)
        self.cooldown_down.on_key_release(symbol, modifiers)
        self.cooldown_left.on_key_release(symbol, modifiers)
        self.cooldown_right.on_key_release(symbol, modifiers)



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
