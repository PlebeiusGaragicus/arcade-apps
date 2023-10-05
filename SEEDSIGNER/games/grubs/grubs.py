import random
from dataclasses import dataclass

from PIL import Image, ImageDraw

from seedsigner.hardware.buttons import HardwareButtonsConstants
from modules.games import BaseGameScreen

MOVEMENT_SPEED = 6

@dataclass
class Handler(BaseGameScreen):
    def setup(self):
        self.snake = [(20, 20), (30, 20), (40, 20)]
        self.direction = 'RIGHT'
        self.fruit = None

    def update(self):
        # Add the next position of the snake to the snake's body
        head = self.snake[0]
        if self.direction == 'RIGHT':
            self.snake.insert(0, (head[0] + MOVEMENT_SPEED, head[1]))
        elif self.direction == 'DOWN':
            self.snake.insert(0, (head[0], head[1] + MOVEMENT_SPEED))
        elif self.direction == 'LEFT':
            self.snake.insert(0, (head[0] - MOVEMENT_SPEED, head[1]))
        elif self.direction == 'UP':
            self.snake.insert(0, (head[0], head[1] - MOVEMENT_SPEED))

        # If the snake has eaten the fruit
        if self.fruit == self.snake[0]:
            self.fruit = None
        else:
            # Remove the tail of the snake (since it has not eaten)
            self.snake.pop()

        # If no fruit, create a new fruit
        if not self.fruit:
            self.fruit = (random.randint(0, 240//MOVEMENT_SPEED)*MOVEMENT_SPEED, 
                          random.randint(0, 240//MOVEMENT_SPEED)*MOVEMENT_SPEED)

    def input(self, input):
        if HardwareButtonsConstants.KEY_DOWN in input:
            self.direction = 'DOWN'
        if HardwareButtonsConstants.KEY_UP in input:
            self.direction = 'UP'
        if HardwareButtonsConstants.KEY_LEFT in input:
            self.direction = 'LEFT'
        if HardwareButtonsConstants.KEY_RIGHT in input:
            self.direction = 'RIGHT'

    def draw(self):
        image = Image.new("RGB", (240, 240), "black")
        draw = ImageDraw.Draw(image)

        # Draw the snake
        for position in self.snake:
            draw.rectangle((position[0], position[1], position[0] + MOVEMENT_SPEED, position[1] + MOVEMENT_SPEED), fill="white")

        # Draw the fruit
        if self.fruit:
            draw.ellipse((self.fruit[0], self.fruit[1], self.fruit[0] + MOVEMENT_SPEED, self.fruit[1] + MOVEMENT_SPEED), fill="red")

        with self.renderer.lock:
            self.renderer.disp.ShowImage(image, 0, 0)