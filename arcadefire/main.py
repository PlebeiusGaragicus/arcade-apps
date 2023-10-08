import arcade

from arcadefire.game import MyGame
from arcadefire.config import SCREEN_WIDTH, SCREEN_HEIGHT

def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()
