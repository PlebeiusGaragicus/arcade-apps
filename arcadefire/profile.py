# import arcade
# import cProfile
# from arcadefire.game import MyGame
# from arcadefire.config import SCREEN_WIDTH, SCREEN_HEIGHT

# class ProfileGame(MyGame):
#     def __init__(self, screen_width, screen_height):
#         super().__init__(screen_width, screen_height)
#         self.profiler = cProfile.Profile()

#     def update(self, delta_time):
#         self.profiler.enable()
#         super().update(delta_time)
#         self.profiler.disable()

#     def on_close(self):
#         self.profiler.print_stats(sort="cumulative")
#         super().on_close()

# def main():
#     game = ProfileGame(SCREEN_WIDTH, SCREEN_HEIGHT)
#     arcade.run()

# if __name__ == "__main__":
#     main()
