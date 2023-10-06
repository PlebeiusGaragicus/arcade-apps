import random
from dataclasses import dataclass

from PIL import Image, ImageDraw

from seedsigner.hardware.buttons import HardwareButtonsConstants

from modules.games import BaseGameScreen
from modules.games.color import *


print("SNEK MODULE IS BEING LOADED AND RUN TOP-LEVEL!")


SNEK_GREEN = (90, 255, 50)
SNEK_DEAD = (30, 90, 20)
FOOD_COLOR = (255, 99, 99)
SNAKE_COLOR = BRIGHT_GREEN

BORDER_WIDTH = 4
SCREEN_SIZE = (240, 240)
FOOD_SIZE = 6
FOOD_TOLERANCE = 40
SNAKE_INIT_SIZE = 9
SNAKE_STARTING_POS = (20, 20)
SNAKE_INIT_SPEED_X = -2
SNAKE_INIT_SPEED_Y = -4
TOP_SPEED = 5
TOP_TOTAL_SPEED = 8


class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = FOOD_SIZE
    
    def draw(self, drawer):
        drawer.rectangle((self.x, self.y, self.x + self.size, self.y + self.size), fill=FOOD_COLOR)

    def is_eaten(self, snake):
        head = snake[0]
        return head[0] == self.x and head[1] == self.y
    
    def snake_is_close(self, snake):
        head = snake[0]
        return (head[0] - self.x) ** 2 + (head[1] - self.y) ** 2 < FOOD_TOLERANCE



@dataclass
class Handler(BaseGameScreen):
    def setup(self):
        self.bg = Image.new("RGB", (240, 240), "black")
        drawer = ImageDraw.Draw(self.bg)

        # Draw the border
        outer_border = (0, 0, 240, 240)
        inner_border = (BORDER_WIDTH, BORDER_WIDTH, 240-BORDER_WIDTH, 240-BORDER_WIDTH)
        drawer.rectangle(outer_border, fill="red")  # Draw outer border
        drawer.rectangle(inner_border, fill="black")  # Draw inner border to create the border illusion

        self.bigness = SNAKE_INIT_SIZE
        self.speed_x = SNAKE_INIT_SPEED_X
        self.speed_y = SNAKE_INIT_SPEED_Y

        # self.snake = [(20, 20), (22, 24), (24, 28), (26, 32), (28, 36)]
        self.snake = []
        for i in range(10):
            self.snake.append((SNAKE_STARTING_POS[0] + i * self.speed_x, SNAKE_STARTING_POS[1] + i * self.speed_y))

        self.food = [Food(200, 150)]


    def update(self):
        head = self.snake[0]
        new_head = (head[0] + self.speed_x, head[1] + self.speed_y)

        if new_head[0] < BORDER_WIDTH:
            self.speed_x = -self.speed_x
            new_head = (BORDER_WIDTH, new_head[1])

        if new_head[0] > SCREEN_SIZE[0] - BORDER_WIDTH - self.bigness:
            self.speed_x = -self.speed_x
            new_head = (SCREEN_SIZE[0] - BORDER_WIDTH - self.bigness, new_head[1])

        if new_head[1] < BORDER_WIDTH:
            self.speed_y = -self.speed_y
            new_head = (new_head[0], BORDER_WIDTH)
        
        if new_head[1] > SCREEN_SIZE[1] - BORDER_WIDTH - self.bigness:
            self.speed_y = -self.speed_y
            new_head = (new_head[0], SCREEN_SIZE[1] - BORDER_WIDTH - self.bigness) # hmmm

        self.snake.insert(0, new_head)
        self.snake.pop()

        for food in self.food:
            if food.snake_is_close(self.snake):
                self.food.remove(food)
                self.food.append(Food(random.randint(BORDER_WIDTH, SCREEN_SIZE[0] - BORDER_WIDTH - 6), random.randint(BORDER_WIDTH, SCREEN_SIZE[1] - BORDER_WIDTH - 6)))
                # self.snake.append(self.snake[-1])
    
    # def change_speed(self, x_delta: int = None, y_delta: int = None) -> None:
    #     if self.speed_x != 0:
    #         self.speed_x -= x_delta if self.speed_x > 0 else -x_delta
    #     if self.speed_y != 0:
    #         self.speed_y -= y_delta if self.speed_y > 0 else -y_delta

    def change_speed(self, delta: int) -> None:
        if self.speed_x != 0:
            self.speed_x -= delta if self.speed_x > 0 else -delta
        if self.speed_y != 0:
            self.speed_y -= delta if self.speed_y > 0 else -delta

    def input(self, input):
        if HardwareButtonsConstants.KEY2 in input:
            pass
            # self.change_speed(delta=1)

        if HardwareButtonsConstants.KEY3 in input:
            pass
            # self.change_speed(delta=-1)

        if HardwareButtonsConstants.KEY_PRESS in input:
            self.speed_x = 0
            self.speed_y = 0

        if HardwareButtonsConstants.KEY_DOWN in input:
            if self.speed_y > TOP_SPEED:
                self.speed_y = TOP_SPEED
                if self.speed_x != 0:
                    self.speed_x -= 1 if self.speed_x > 0 else -1
            elif self.speed_y < -TOP_SPEED:
                self.speed_y = -TOP_SPEED
                if self.speed_x != 0:
                    self.speed_x -= 1 if self.speed_x > 0 else -1
            else:
                self.speed_y += 1
        elif HardwareButtonsConstants.KEY_UP in input:
            if self.speed_y > TOP_SPEED:
                self.speed_y = TOP_SPEED
                if self.speed_x != 0:
                    self.speed_x -= 1 if self.speed_x > 0 else -1
            elif self.speed_y < -TOP_SPEED:
                self.speed_y = -TOP_SPEED
                if self.speed_x != 0:
                    self.speed_x -= 1 if self.speed_x > 0 else -1
            else:
                self.speed_y -= 1

        if HardwareButtonsConstants.KEY_LEFT in input:
            if self.speed_x > TOP_SPEED:
                self.speed_x = TOP_SPEED
                if self.speed_y != 0:
                    self.speed_y -= 1 if self.speed_y > 0 else -1
            elif self.speed_x < -TOP_SPEED:
                self.speed_x = -TOP_SPEED
                if self.speed_y != 0:
                    self.speed_y -= 1 if self.speed_y > 0 else -1
            else:
                self.speed_x -= 1
        elif HardwareButtonsConstants.KEY_RIGHT in input:
            if self.speed_x > TOP_SPEED:
                self.speed_x = TOP_SPEED
                if self.speed_y != 0:
                    self.speed_y -= 1 if self.speed_y > 0 else -1
            elif self.speed_x < -TOP_SPEED:
                self.speed_x = -TOP_SPEED
                if self.speed_y != 0:
                    self.speed_y -= 1 if self.speed_y > 0 else -1
            else:
                self.speed_x += 1


    def draw(self):
        image = self.bg.copy()
        drawer = ImageDraw.Draw(image)

        # Draw the food
        for food in self.food:
            food.draw(drawer)

        # for i in range(len(self.snake) - 1):
        #     drawer.rectangle((self.snake[i][0], self.snake[i][1], self.snake[i][0] + self.bigness - i, self.snake[i][1] + self.bigness - i), fill=SNAKE_COLOR)

        # for position in self.snake:
            # drawer.rectangle((position[0], position[1], position[0] + self.bigness, position[1] + self.bigness), fill="white")

        for i in range(len(self.snake) - 1):
            drawer.line(
            [self.snake[i][0] + self.bigness / 2, self.snake[i][1] + self.bigness / 2, self.snake[i + 1][0] + self.bigness / 2, self.snake[i + 1][1] + self.bigness / 2],
            fill=SNAKE_COLOR,
            # width= i + self.bigness)
            # width=i + 1)
            width=self.bigness - i)

        with self.renderer.lock:
            self.renderer.disp.ShowImage(image, 0, 0)
