import time
import math
import logging
logger = logging.getLogger()

import arcade


HOLD_TO_QUIT_SECONDS = 1.5

TOP_BAR_HEIGHT = 30

# move to config.py ???
window_width, window_height = arcade.get_display_size()


COOLDOWN_DIRECTIONAL_SECONDS = 0.1


# These can be anything, just make sure they're unique
KEY_UP = arcade.key.W
KEY_DOWN = arcade.key.S
KEY_LEFT = arcade.key.A
KEY_RIGHT = arcade.key.D




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
    def __init__(self, key, cooldown_seconds):
        self.key = key
        self.cooldown_seconds = cooldown_seconds
        self.pressed = False
        self.last_pressed_time = None

    def run(self, key: int = None):

        # for the on_key_press() function
        if key is not None:
            if key == self.key:
                self.pressed = True
                return False
            else:
                return False
        
        # for the on_update() function
        else:
            if self.pressed is True:
                if self.last_pressed_time is None or time.time() > self.last_pressed_time + self.cooldown_seconds:
                    self.last_pressed_time = time.time()
                    return True
                else:
                    print(f"cooldown for {self.key} not ready yet. {time.time() - self.last_pressed_time}")
                    return False
            else:
                return False

    def on_key_release(self, key: int):
        if key == self.key:
            self.pressed = False
            return True
        else:
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

        self.cooldown_keys = {
            KEY_UP: CooldownKey(arcade.key.UP, COOLDOWN_DIRECTIONAL_SECONDS),
            KEY_DOWN: CooldownKey(arcade.key.DOWN, COOLDOWN_DIRECTIONAL_SECONDS),
            KEY_LEFT: CooldownKey(arcade.key.LEFT, COOLDOWN_DIRECTIONAL_SECONDS),
            KEY_RIGHT: CooldownKey(arcade.key.RIGHT, COOLDOWN_DIRECTIONAL_SECONDS),
        }
        # self.cooldown_left = CooldownKey(arcade.key.LEFT, 0.1)
        # self.cooldown_right = CooldownKey(arcade.key.RIGHT, 0.1)
        # self.cooldown_up = CooldownKey(arcade.key.UP, 0.1)
        # self.cooldown_down = CooldownKey(arcade.key.DOWN, 0.1)



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

        self.handle_cooldown_keys()
        # # if self.cooldown_up.run():
        # if self.cooldown_keys[KEY_UP].run():
        #     logger.info("up")
        #     self.player.dir_y += 1

        # # if self.cooldown_down.run():
        # if self.cooldown_keys[KEY_DOWN].run():
        #     logger.info("down")
        #     self.player.dir_y += -1

        # # if self.cooldown_left.run():
        # if self.cooldown_keys[KEY_LEFT].run():
        #     logger.info("left")
        #     self.player.dir_x += -1

        # # if self.cooldown_right.run():
        # if self.cooldown_keys[KEY_RIGHT].run():
        #     logger.info("right")
        #     self.player.dir_x += 1





    def on_draw(self):
        arcade.start_render()

        # show life in top left corner
        arcade.draw_text(f"Life: {self.life}", 10, self.window.height * 0.9, arcade.color.WHITE, font_size=20, anchor_x="left")

        # show player x and y direction
        arcade.draw_text(f"dir_x: {self.player.dir_x} / dir_y: {self.player.dir_y}", window_width // 2, self.window.height * 0.9, arcade.color.YELLOW, font_size=20, anchor_x="center")

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



    def on_key_press(self, key: int, modifiers: int):

        print(modifiers)

        if key == None:
            logger.critical("FUCK FUCK")

        if key == arcade.key.ESCAPE:
            logger.info("escape")
            self.escape_pressed_time = time.time()
            self.paused = True

        elif key == arcade.key.P:
            logger.info("pause")
            self.paused = not self.paused
        
        if self.paused:
            return

        elif key == arcade.key.SPACE:
            logger.info("space")
            self.life += 10

        print("key: ", key)

        self.handle_cooldown_keys(key)
        # # these can't be elif!
        # if self.cooldown_up.on_key_press(key):
        #     logger.info("up")
        #     self.player.dir_y += 1
        # if self.cooldown_down.on_key_press(key):
        #     logger.info("down")
        #     self.player.dir_y += -1
        # if self.cooldown_left.on_key_press(key):
        #     logger.info("left")
        #     self.player.dir_x += -1
        # if self.cooldown_right.on_key_press(key):
        #     logger.info("right")
        #     self.player.dir_x += 1

    
    def on_key_release(self, key: int, modifiers: int):
        if key == arcade.key.ESCAPE:
            logger.info("escape released")
            self.escape_pressed_time = None
            self.paused = False
        
        if self.paused:
            return

        # self.cooldown_up.on_key_release(key)
        # self.cooldown_down.on_key_release(key)
        # self.cooldown_left.on_key_release(key)
        # self.cooldown_right.on_key_release(key)
        self.cooldown_keys[KEY_UP].on_key_release(key)
        self.cooldown_keys[KEY_DOWN].on_key_release(key)
        self.cooldown_keys[KEY_LEFT].on_key_release(key)
        self.cooldown_keys[KEY_RIGHT].on_key_release(key)



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


    def handle_cooldown_keys(self, key: int = None):
        # if self.cooldown_up.run():
        if self.cooldown_keys[KEY_UP].run(key=key):
            logger.info("up")
            self.player.dir_y += 1

        # if self.cooldown_down.run():
        if self.cooldown_keys[KEY_DOWN].run(key=key):
            logger.info("down")
            self.player.dir_y += -1

        # if self.cooldown_left.run():
        if self.cooldown_keys[KEY_LEFT].run(key=key):
            logger.info("left")
            self.player.dir_x += -1

        # if self.cooldown_right.run():
        if self.cooldown_keys[KEY_RIGHT].run(key=key):
            logger.info("right")
            self.player.dir_x += 1
