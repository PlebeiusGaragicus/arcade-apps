import math
import random
from dataclasses import dataclass

import arcade
import pymunk
from pymunk.vec2d import Vec2d

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BALL_RADIUS = 20



@dataclass
class PropertiesofNature:
    gravity = -700
    friction = 0.5
    elasticity = 0.2
    damping = 0.976
    time_step = 1/60.0

    class Boundary:
        elasticity = 0.23
        friction = 0.7
    
    class Obstacle:
        elasticity = 0.6
        friction = 0.5
    
    class Ball:
        elasticity = 1
        friction = 0.5

    class Wall:
        elasticity = 0.2
        friction = 0.5




class Ball:
    def __init__(self, x, y, dx, dy, radius=BALL_RADIUS):
        mass = 1
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        self.body = pymunk.Body(mass, inertia)
        self.body.position = x, y
        self.body.velocity = dx, dy

        self.shape = pymunk.Circle(self.body, radius)
        self.shape.elasticity = 1
        self.shape.friction = 0.5
        self.shape.collision_type = 1

        self.sprite = arcade.SpriteCircle(radius, arcade.color.RED)
        self.sprite.center_x = x
        self.sprite.center_y = y

    def sync_sprite(self):
        self.sprite.center_x = self.body.position.x
        self.sprite.center_y = self.body.position.y
        self.sprite.angle = math.degrees(self.body.angle)

    def draw(self):
        self.sync_sprite()
        self.sprite.draw()




class MyGame(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height, "Enhanced Bouncing Ball Simulation with PyMunk and Arcade")
        arcade.set_background_color(arcade.color.WHITE)
        self.space = pymunk.Space()
        self.space.gravity = (0, PropertiesofNature.gravity)

        # Introduce damping to simulate air resistance
        self.space.damping = 0.976  # Value between 0 and 1; 0 means no damping



        self.balls = []

        for _ in range(40):
            x = random.randint(BALL_RADIUS, SCREEN_WIDTH - BALL_RADIUS)
            y = random.randint(BALL_RADIUS, SCREEN_HEIGHT - BALL_RADIUS)
            dx = random.randint(-150, 150)
            dy = random.randint(-150, 150)

            self.balls.append(Ball(x, y, dx, dy))

        for ball in self.balls:
            self.space.add(ball.body, ball.shape)

        # Boundary walls
        walls = [
            pymunk.Segment(self.space.static_body, (0, 0), (0, SCREEN_HEIGHT), 1),
            pymunk.Segment(self.space.static_body, (0, SCREEN_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT), 1),
            pymunk.Segment(self.space.static_body, (SCREEN_WIDTH, SCREEN_HEIGHT), (SCREEN_WIDTH, 0), 1),
            pymunk.Segment(self.space.static_body, (SCREEN_WIDTH, 0), (0, 0), 1)
        ]

        for wall in walls:
            wall.elasticity = 0.23
            wall.friction = 0.7
        self.space.add(*walls)

        # Adding a static polygon obstacle in the middle
        # TRIANGLE
        vertices = [(x+SCREEN_WIDTH//2, y+SCREEN_HEIGHT//2) for x, y in [(0, -50), (-50, 50), (50, 50)]]
        obstacle = pymunk.Poly(self.space.static_body, vertices)

        obstacle.elasticity = 0.2
        obstacle.friction = 0.8
        self.space.add(obstacle)


    def on_draw(self):
        arcade.start_render()
        for ball in self.balls:
            ball.draw()
        self.draw_obstacle([(x+SCREEN_WIDTH//2, y+SCREEN_HEIGHT//2) for x, y in [(0, -50), (-50, 50), (50, 50)]])

    def update(self, delta_time):
        physics_timestep = 1/60.0
        self.space.step(physics_timestep)

    def handle_collision(self, arbiter, space, data):
        return True
    
    def draw_obstacle(self, vertices, color=arcade.color.GRAY):
        arcade.draw_polygon_filled(vertices, color)

    def reset_simulation(self):
        # Clear all bodies and shapes from the space
        for shape in self.space.shapes:
            self.space.remove(shape)
        for body in self.space.bodies:
            self.space.remove(body)

        # Reinitialize the balls
        self.balls = []
        for _ in range(40):
            x = random.randint(BALL_RADIUS, SCREEN_WIDTH - BALL_RADIUS)
            y = random.randint(BALL_RADIUS, SCREEN_HEIGHT - BALL_RADIUS)
            dx = random.randint(-150, 150)
            dy = random.randint(-150, 150)
            self.balls.append(Ball(x, y, dx, dy))

        for ball in self.balls:
            self.space.add(ball.body, ball.shape)

        # Reinitialize the boundary walls
        walls = [
            pymunk.Segment(self.space.static_body, (0, 0), (0, SCREEN_HEIGHT), 1),
            pymunk.Segment(self.space.static_body, (0, SCREEN_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT), 1),
            pymunk.Segment(self.space.static_body, (SCREEN_WIDTH, SCREEN_HEIGHT), (SCREEN_WIDTH, 0), 1),
            pymunk.Segment(self.space.static_body, (SCREEN_WIDTH, 0), (0, 0), 1)
        ]
        for wall in walls:
            wall.elasticity = 0.2
            wall.friction = 0.5
        self.space.add(*walls)

        # Reinitialize the obstacle
        vertices = [(x+SCREEN_WIDTH//2, y+SCREEN_HEIGHT//2) for x, y in [(0, -50), (-50, 50), (50, 50)]]
        obstacle = pymunk.Poly(self.space.static_body, vertices)
        obstacle.elasticity = 0.6
        obstacle.friction = 0.5
        self.space.add(obstacle)
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.reset_simulation()

if __name__ == "__main__":
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()
