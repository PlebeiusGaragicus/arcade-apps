import arcade

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BALL_RADIUS = 20

class Ball:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def move(self):
        # Move the ball
        self.x += self.dx
        self.y += self.dy

        # Bounce on edges
        if self.x < BALL_RADIUS or self.x > SCREEN_WIDTH - BALL_RADIUS:
            self.dx = -self.dx
        if self.y < BALL_RADIUS or self.y > SCREEN_HEIGHT - BALL_RADIUS:
            self.dy = -self.dy

    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, BALL_RADIUS, arcade.color.RED)

class MyGame(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height, "Bouncing Ball Simulation")

        arcade.set_background_color(arcade.color.WHITE)
        self.ball = Ball(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, 3, 4)

    def on_draw(self):
        arcade.start_render()
        self.ball.draw()

    def update(self, delta_time):
        self.ball.move()

if __name__ == "__main__":
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()
