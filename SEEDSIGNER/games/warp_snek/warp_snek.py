DEBUG = False

import random
import time
from dataclasses import dataclass

from PIL import Image, ImageDraw

from seedsigner.hardware.buttons import HardwareButtonsConstants
# from seedsigner.gui.components import GUIConstants, FontAwesomeIconConstants
from seedsigner.gui.components import load_image
# from seedsigner.gui.screens.game_screens import BaseGameScreen
from modules.games import BaseGameScreen


# from helpers import lerp
# from seedsigner.gui.screens.game_screens import lerp
# from games.helpers import *
from modules.games.color import lerp
from modules.games.fonts import FontAwesomeIcons



BORDER_WIDTH = 4
SCREEN_SIZE = (240, 240)

SNAKE_STARTING_HEALTH = 120 ##############################       <----------

SNAKE_COLOR_HEALTHY = (90, 255, 50)
SNAKE_COLOR_DEATH = (30, 90, 20)
SNAKE_INIT_SIZE = 8
SNAKE_STARTING_POS = (20, 20)
SNAKE_INIT_SPEED_X = -2
SNAKE_INIT_SPEED_Y = -4
TOP_SPEED = 13

FOOD_COLOR = (255, 99, 99)
FOOD_SIZE = 6
FOOD_EATING_DISTANCE = 35
FOOD_MAX_COUNT = 25
FOOD_LIFE_POWER = 12

class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = FOOD_SIZE
        # random color
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
    
    def draw(self, drawer: ImageDraw):
        drawer.rectangle((self.x, self.y, self.x + self.size, self.y + self.size), fill=self.color)

    def is_eaten(self, snake):
        head = snake[0]
        return head[0] == self.x and head[1] == self.y
    
    def snake_is_close(self, snake):

        for segment in snake:
            if (segment[0] - self.x) ** 2 + (segment[1] - self.y) ** 2 < FOOD_EATING_DISTANCE:
                return True
        # head = snake[0]
        # return (head[0] - self.x) ** 2 + (head[1] - self.y) ** 2 < FOOD_EATING_DISTANCE


class Snek:
    def __init__(self, x, y):
        # TODO change this to a property???
        self.life = SNAKE_STARTING_HEALTH # you have 100 frames to live.. unless you keep eating
        self.bigness = SNAKE_INIT_SIZE
        self.speed_x = x
        self.speed_y = y
        print(f"{self.life=}")

        self.body = []
        for i in range(10):
            self.body.append((SNAKE_STARTING_POS[0] + i * self.speed_x, SNAKE_STARTING_POS[1] + i * self.speed_y))

    def change_speed_cap(self, x_delta: int = None, y_delta: int = None) -> None:
        if x_delta is not None:
            if abs(self.speed_x) > TOP_SPEED:
                self.speed_x = TOP_SPEED if self.speed_x > 0 else -TOP_SPEED # cap to TOP SPEED
                if self.speed_y != 0: # ... the goal is to reduce the X speed by 1, if not zero
                    self.speed_y -= 1 if self.speed_y > 0 else -1 # move the X speed down (towards zero)
            else:
                self.speed_x += x_delta # do the speed increase

        if y_delta is not None:
            if abs(self.speed_y) > TOP_SPEED:
                self.speed_y = TOP_SPEED if self.speed_y > 0 else -TOP_SPEED # cap to TOP SPEED
                if self.speed_x != 0: # ... the goal is to reduce the X speed by 1, if not zero
                    self.speed_x -= 1 if self.speed_x > 0 else -1 # move the X speed down (towards zero)
            else:
                self.speed_y += y_delta # do the speed increase

    def change_speed(self, delta: int) -> None:
        if abs(self.speed_x) > 1: # don't slow to zero speed (because the speed up button will no longer work to speed up)
            if self.speed_x != 0:
                self.speed_x -= delta if self.speed_x > 0 else -delta
        if abs(self.speed_y) > 1:
            if self.speed_y != 0:
                self.speed_y -= delta if self.speed_y > 0 else -delta

    def update(self):
        self.life -= 1
        print(self.life)

        head = self.body[0]
        new_head = (head[0] + self.speed_x, head[1] + self.speed_y)

        if new_head[0] < BORDER_WIDTH:
            self.speed_x = -self.speed_x
            new_head = (BORDER_WIDTH, new_head[1])

        if new_head[0] > SCREEN_SIZE[0] - BORDER_WIDTH - 6:
            self.speed_x = -self.speed_x
            new_head = (SCREEN_SIZE[0] - BORDER_WIDTH - 6, new_head[1])

        if new_head[1] < BORDER_WIDTH:
            self.speed_y = -self.speed_y
            new_head = (new_head[0], BORDER_WIDTH)
        
        if new_head[1] > SCREEN_SIZE[1] - BORDER_WIDTH - 6:
            self.speed_y = -self.speed_y
            new_head = (new_head[0], SCREEN_SIZE[1] - BORDER_WIDTH - 6) # hmmm

        self.body.insert(0, new_head)
        self.body.pop()

    def draw(self, drawer: ImageDraw):
        # for position in self.body:
        #     drawer.rectangle((position[0], position[1], position[0] + self.bigness, position[1] + self.bigness), fill="white")

        for i in range(len(self.body) - 1):
            drawer.line(
            [self.body[i][0] + self.bigness / 2, self.body[i][1] + self.bigness / 2, self.body[i + 1][0] + self.bigness / 2, self.body[i + 1][1] + self.bigness / 2],
            fill=lerp(SNAKE_COLOR_DEATH, SNAKE_COLOR_HEALTHY, self.life / 100),
            width=self.bigness - i)


@dataclass
class Handler(BaseGameScreen):
    display_name: str = "Warp Snek"
    font_icon: FontAwesomeIcons = FontAwesomeIcons.SLASH
    # intro_image_filename: str = None

    def setup(self):
        self.bg = Image.new("RGB", (240, 240), "black")
        drawer = ImageDraw.Draw(self.bg)

        # Draw the border
        outer_border = (0, 0, 240, 240)
        inner_border = (BORDER_WIDTH, BORDER_WIDTH, 240-BORDER_WIDTH, 240-BORDER_WIDTH)
        drawer.rectangle(outer_border, fill="red")  # Draw outer border
        drawer.rectangle(inner_border, fill="black")  # Draw inner border to create the border illusion

        self.snake = Snek(SNAKE_INIT_SPEED_X, SNAKE_INIT_SPEED_Y)

        # self.life = SNAKE_STARTING_HEALTH # you have 100 frames to live.. unless you keep eating
        # print(f"{self.life=}")
        # self.bigness = SNAKE_INIT_SIZE
        # self.speed_x = SNAKE_INIT_SPEED_X
        # self.speed_y = SNAKE_INIT_SPEED_Y

        # self.snake = [(20, 20), (22, 24), (24, 28), (26, 32), (28, 36)]
        # self.snake = []
        # for i in range(10):
        #     self.snake.append((SNAKE_STARTING_POS[0] + i * self.speed_x, SNAKE_STARTING_POS[1] + i * self.speed_y))

        # self.food = [Food(200, 150)]
        self.food = []
        self.food.append(Food(random.randint(BORDER_WIDTH, SCREEN_SIZE[0] - BORDER_WIDTH - 6), random.randint(BORDER_WIDTH, SCREEN_SIZE[1] - BORDER_WIDTH - 6)))


    def update(self):
        self.snake.update()

        if self.snake.life <= 0:
            self.won_the_game = None
            self.alive = False

        # self.life -= 1
        # print(self.life)

        # if self.life <= 0:
        #     self.won_the_game = None
        #     self.alive = False

        # head = self.snake[0]
        # new_head = (head[0] + self.speed_x, head[1] + self.speed_y)

        # if new_head[0] < BORDER_WIDTH:
        #     self.speed_x = -self.speed_x
        #     new_head = (BORDER_WIDTH, new_head[1])

        # if new_head[0] > SCREEN_SIZE[0] - BORDER_WIDTH - 6:
        #     self.speed_x = -self.speed_x
        #     new_head = (SCREEN_SIZE[0] - BORDER_WIDTH - 6, new_head[1])

        # if new_head[1] < BORDER_WIDTH:
        #     self.speed_y = -self.speed_y
        #     new_head = (new_head[0], BORDER_WIDTH)
        
        # if new_head[1] > SCREEN_SIZE[1] - BORDER_WIDTH - 6:
        #     self.speed_y = -self.speed_y
        #     new_head = (new_head[0], SCREEN_SIZE[1] - BORDER_WIDTH - 6) # hmmm

        # self.snake.insert(0, new_head)
        # self.snake.pop()

        # add food
        if len(self.food) < FOOD_MAX_COUNT:
            if random.randint(0, 100) < 90:
                self.food.append(Food(random.randint(BORDER_WIDTH, SCREEN_SIZE[0] - BORDER_WIDTH - 6), random.randint(BORDER_WIDTH, SCREEN_SIZE[1] - BORDER_WIDTH - 6)))

        for food in self.food:
            if food.snake_is_close(self.snake.body):
                self.snake.life += FOOD_LIFE_POWER
                self.food.remove(food)
                self.food.append(Food(random.randint(BORDER_WIDTH, SCREEN_SIZE[0] - BORDER_WIDTH - 6), random.randint(BORDER_WIDTH, SCREEN_SIZE[1] - BORDER_WIDTH - 6)))


    def input(self, input):
        if HardwareButtonsConstants.KEY2 in input:
            self.snake.change_speed(delta=-1)

        if HardwareButtonsConstants.KEY3 in input:
            self.snake.change_speed(delta=1)

        if HardwareButtonsConstants.KEY_PRESS in input:
            self.snake.speed_x = 0
            self.snake.speed_y = 0

        if HardwareButtonsConstants.KEY_DOWN in input:
            self.snake.change_speed_cap(y_delta=1)

        elif HardwareButtonsConstants.KEY_UP in input:
            self.snake.change_speed_cap(y_delta=-1)

        if HardwareButtonsConstants.KEY_LEFT in input:
            self.snake.change_speed_cap(x_delta=-1)

        elif HardwareButtonsConstants.KEY_RIGHT in input:
            self.snake.change_speed_cap(x_delta=1)


    def draw(self):
        image = self.bg.copy()
        drawer = ImageDraw.Draw(image)

        # Draw the food
        for food in self.food:
            food.draw(drawer)

        self.snake.draw(drawer)

        with self.renderer.lock:
            self.renderer.disp.ShowImage(image, 0, 0)
