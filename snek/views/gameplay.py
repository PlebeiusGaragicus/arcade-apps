import random

import pygame

from snek.app import App
from snek.gamestate import GameState
from snek.config import *


class Gameplay(GameState):
    def __init__(self):
        super().__init__()
        # TODO: I'm not sure how to do this best...
        self.snake = None
        self.direction = None
        self.food = None
        self.grow: bool = None


    def setup(self):
        self.snake = [(5, 5), (4, 5), (3, 5)]
        self.direction = (1, 0)  # Right
        self.food = (random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1),
                     random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1))
        self.grow = False


    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.direction != (0, 1):
                self.direction = (0, -1)
            elif event.key == pygame.K_DOWN and self.direction != (0, -1):
                self.direction = (0, 1)
            elif event.key == pygame.K_LEFT and self.direction != (1, 0):
                self.direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and self.direction != (-1, 0):
                self.direction = (1, 0)

    def update(self):
        head_x, head_y = self.snake[0]
        new_x, new_y = self.direction
        new_head = ((head_x + new_x) % (SCREEN_WIDTH // CELL_SIZE), (head_y + new_y) % (SCREEN_HEIGHT // CELL_SIZE))

        if new_head in self.snake:
            # manager.change_state("game_over")
            App.get_instance().manager.change_state("game_over")
            return

        self.snake.insert(0, new_head)
        if not self.grow:
            self.snake.pop()
        else:
            self.grow = False

        if new_head == self.food:
            self.grow = True
            self.food = (random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1),
                         random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1))

    def draw(self, screen):
        screen.fill(BLACK)
        for segment in self.snake:
            pygame.draw.rect(screen, GREEN, (segment[0]*CELL_SIZE, segment[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, RED, (self.food[0]*CELL_SIZE, self.food[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
