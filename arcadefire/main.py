# import arcade

# from arcadefire.game import MyGame
# from arcadefire.config import SCREEN_WIDTH, SCREEN_HEIGHT

# def main():
#     game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
#     arcade.run()



import arcade
from arcadefire.game import MyGame, ProfileGame
from arcadefire.config import SCREEN_WIDTH, SCREEN_HEIGHT

def main(profile=False):
    if profile:
        game = ProfileGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    else:
        game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()
