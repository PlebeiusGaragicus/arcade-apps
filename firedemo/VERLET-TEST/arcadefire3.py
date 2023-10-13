import math
import random
from dataclasses import dataclass

import arcade
import pymunk

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BALL_RADIUS = 20

@dataclass
class PropertiesofNature:
    gravity: float = -700
    friction: float = 0.5
    elasticity: float = 0.2
    damping: float = 0.976
    time_step: float = 1/60.0

    class Boundary:
        elasticity: float = 0.23
        friction: float = 0.7

    class Obstacle:
        elasticity: float = 0.4
        friction: float = 0.5

    class Ball:
        elasticity: float = 0.3
        friction: float = 0.7

    class Wall:
        elasticity: float = 0.2
        friction: float = 0.5

    class Temperature:
        ambient: float = 300.0  # Room temperature in Kelvin
        max_temperature: float = 2000.0  # White color

class Ball:
    def __init__(self, x, y, dx, dy, radius=BALL_RADIUS, temperature=PropertiesofNature.Temperature.ambient):
        mass = 1
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        self.body = pymunk.Body(mass, inertia)
        self.body.position = x, y
        self.body.velocity = dx, dy

        # Use properties from PropertiesofNature class
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.elasticity = PropertiesofNature.Ball.elasticity
        self.shape.friction = PropertiesofNature.Ball.friction
        self.temperature = temperature
        self.shape.collision_type = 1

        self.sprite = arcade.SpriteCircle(radius, arcade.color.RED)
        self.sprite.center_x = x
        self.sprite.center_y = y

    def sync_sprite(self):
        self.sprite.center_x = self.body.position.x
        self.sprite.center_y = self.body.position.y
        self.sprite.angle = math.degrees(self.body.angle)

    def get_color_based_on_temperature(self):
        max_temp = PropertiesofNature.Temperature.max_temperature
        ratio = self.temperature / max_temp
        if ratio < 0.5:
            # Transition from black to red
            return (int(255 * 2 * ratio), 0, 0)
        else:
            # Transition from red to white
            ratio = 2 * (ratio - 0.5)
            return (255, int(255 * ratio), int(255 * ratio))

    def transfer_temperature(self, other_ball):
        # Take the average of the two temperatures
        new_temperature = (self.temperature + other_ball.temperature) / 2
        self.temperature = new_temperature
        other_ball.temperature = new_temperature

    def draw(self):
        self.sync_sprite()
        self.sprite.color = self.get_color_based_on_temperature()
        self.sprite.draw()

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

if __name__ == "__main__":
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()
