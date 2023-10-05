from time import sleep
import arcade
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Snake Game"
TILE_SIZE = 20
SNAKE_SPEED = 5

class Snake(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.snake_list = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.snake_speed = SNAKE_SPEED
        self.apple_x = 0
        self.apple_y = 0
        self.change_x = TILE_SIZE
        self.change_y = 0

        self.spawn_apple()

    def spawn_apple(self):
        self.apple_x = random.randint(0, (SCREEN_WIDTH // TILE_SIZE) - 1) * TILE_SIZE
        self.apple_y = random.randint(0, (SCREEN_HEIGHT // TILE_SIZE) - 1) * TILE_SIZE

    def on_draw(self):
        arcade.start_render()
        
        for x, y in self.snake_list:
            arcade.draw_xywh_rectangle_filled(x, y, TILE_SIZE, TILE_SIZE, arcade.color.GREEN)
        
        arcade.draw_xywh_rectangle_filled(self.apple_x, self.apple_y, TILE_SIZE, TILE_SIZE, arcade.color.RED)

    def update(self, delta_time):
        sleep(1 / self.snake_speed)

        head_x = self.snake_list[-1][0] + self.change_x
        head_y = self.snake_list[-1][1] + self.change_y
        
        # Check wall collision
        if head_x < 0 or head_x >= SCREEN_WIDTH or head_y < 0 or head_y >= SCREEN_HEIGHT:
            self.close()

        # Check apple collision
        if head_x == self.apple_x and head_y == self.apple_y:
            self.snake_list.append((head_x, head_y))
            self.spawn_apple()
        else:
            self.snake_list.pop(0)
            self.snake_list.append((head_x, head_y))

        # Check self collision
        if len(self.snake_list) != len(set(self.snake_list)):
            self.close()

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.UP and self.change_y == 0:
            self.change_x = 0
            self.change_y = TILE_SIZE
        elif symbol == arcade.key.DOWN and self.change_y == 0:
            self.change_x = 0
            self.change_y = -TILE_SIZE
        elif symbol == arcade.key.LEFT and self.change_x == 0:
            self.change_x = -TILE_SIZE
            self.change_y = 0
        elif symbol == arcade.key.RIGHT and self.change_x == 0:
            self.change_x = TILE_SIZE
            self.change_y = 0

if __name__ == "__main__":
    window = Snake()
    arcade.run()
