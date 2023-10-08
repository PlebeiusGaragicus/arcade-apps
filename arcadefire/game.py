import random

import arcade
import pymunk

from arcadefire.config import BALL_RADIUS, SCREEN_WIDTH, SCREEN_HEIGHT, PropertiesofNature
from arcadefire.balls import Ball



class MyGame(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height, "Enhanced Bouncing Ball Simulation with PyMunk and Arcade")
        arcade.set_background_color(arcade.color.WHITE)
        self.space = pymunk.Space()
        self.space.gravity = (0, PropertiesofNature.gravity)

        handler = self.space.add_collision_handler(1, 1)  # 1 is the collision type for balls
        handler.begin = self.handle_ball_collision


        # Use damping from PropertiesofNature class
        self.space.damping = PropertiesofNature.damping

        self._initialize_balls()
        # self.space.add_collision_handler(1, 1, begin=self.handle_ball_collision)  # 1 is the collision type for balls
        
        # Create boundary walls and obstacle
        self._initialize_boundaries_and_obstacle()

        self._initialize_triangle_obstacle()


    def _initialize_balls(self):
        self.balls = []
        for _ in range(40):
            x = random.randint(BALL_RADIUS, SCREEN_WIDTH - BALL_RADIUS)
            y = random.randint(BALL_RADIUS, SCREEN_HEIGHT - BALL_RADIUS)
            dx = random.randint(-150, 150)
            dy = random.randint(-150, 150)
            self.balls.append(Ball(x, y, dx, dy, temperature=PropertiesofNature.Temperature.ambient))

        # Now adjust the temperature for a subset of balls
        for ball in random.sample(self.balls, 10):
            ball.temperature = random.uniform(PropertiesofNature.Temperature.ambient, PropertiesofNature.Temperature.max_temperature)

        for ball in self.balls:
            self.space.add(ball.body, ball.shape)

    def _initialize_triangle_obstacle(self):
        vertices = [(x+SCREEN_WIDTH//2, y+SCREEN_HEIGHT//2) for x, y in [(0, -50), (-50, 50), (50, 50)]]
        obstacle = pymunk.Poly(self.space.static_body, vertices)
        obstacle.elasticity = PropertiesofNature.Obstacle.elasticity
        obstacle.friction = PropertiesofNature.Obstacle.friction
        self.space.add(obstacle)

    def _initialize_boundaries_and_obstacle(self):
        walls = [
            pymunk.Segment(self.space.static_body, (0, 0), (0, SCREEN_HEIGHT), 1),
            pymunk.Segment(self.space.static_body, (0, SCREEN_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT), 1),
            pymunk.Segment(self.space.static_body, (SCREEN_WIDTH, SCREEN_HEIGHT), (SCREEN_WIDTH, 0), 1),
            pymunk.Segment(self.space.static_body, (SCREEN_WIDTH, 0), (0, 0), 1)
        ]

        for wall in walls:
            wall.elasticity = PropertiesofNature.Boundary.elasticity
            wall.friction = PropertiesofNature.Boundary.friction

        self.space.add(*walls)

        # Adding a static triangular obstacle in the middle
        vertices = [(x+SCREEN_WIDTH//2, y+SCREEN_HEIGHT//2) for x, y in [(0, -50), (-50, 50), (50, 50)]]
        obstacle = pymunk.Poly(self.space.static_body, vertices)
        obstacle.elasticity = PropertiesofNature.Obstacle.elasticity
        obstacle.friction = PropertiesofNature.Obstacle.friction
        self.space.add(obstacle)

    def on_draw(self):
        arcade.start_render()
        for ball in self.balls:
            ball.draw()
        # No need to call draw_obstacle separately, integrate it into _initialize_boundaries_and_obstacle
        self.draw_obstacle([(x+SCREEN_WIDTH//2, y+SCREEN_HEIGHT//2) for x, y in [(0, -50), (-50, 50), (50, 50)]])

    def update(self, delta_time):
        self.space.step(PropertiesofNature.time_step)  # Use time_step from PropertiesofNature

    def handle_collision(self, arbiter, space, data):
        return True
    
    def handle_ball_collision(self, arbiter, space, data):
        ball_a = next(ball for ball in self.balls if ball.shape == arbiter.shapes[0])
        ball_b = next(ball for ball in self.balls if ball.shape == arbiter.shapes[1])
        ball_a.transfer_temperature(ball_b)
        return True
    
    def draw_obstacle(self, vertices, color=arcade.color.GRAY):
        arcade.draw_polygon_filled(vertices, color)

    def reset_simulation(self):
        # Clear all bodies and shapes from the space
        for shape in self.space.shapes:
            self.space.remove(shape)
        for body in self.space.bodies:
            self.space.remove(body)
        
        self.balls = self._initialize_balls()
        for ball in self.balls:
            self.space.add(ball.body, ball.shape)
        
        # Create boundary walls and obstacle
        self._initialize_boundaries_and_obstacle()
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.reset_simulation()
