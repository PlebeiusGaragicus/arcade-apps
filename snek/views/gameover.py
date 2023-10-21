import pygame

from snek.app import App
from snek.gamestate import GameState
from snek.config import *


class GameOver(GameState):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font(None, 74)
        self.text = self.font.render('Game Over', True, WHITE)
        self.text_rect = self.text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50))
        self.restart_text = self.font.render('Press Space to Restart', True, WHITE)
        self.restart_text_rect = self.restart_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50))

    def setup(self):
        pass

    def update(self):
        pass

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                App.get_instance().manager.change_state("gameplay")

    def draw(self, screen):
        screen.fill(BLACK)
        screen.blit(self.text, self.text_rect)
        screen.blit(self.restart_text, self.restart_text_rect)
