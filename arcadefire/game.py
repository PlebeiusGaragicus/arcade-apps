import random
import cProfile

import arcade
import pymunk

from arcadefire.config import BALL_RADIUS, SCREEN_WIDTH, SCREEN_HEIGHT, PropertiesofNature, NUMBER_OF_BALLS
from arcadefire.balls import Ball



class MyGame(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height, "Enhanced Bouncing Ball Simulation with PyMunk and Arcade")
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        self.space = pymunk.Space()
        self.space.gravity = (0, PropertiesofNature.gravity)
        # Use damping from PropertiesofNature class
        self.space.damping = PropertiesofNature.damping

        handler = self.space.add_collision_handler(1, 1)  # 1 is the collision type for balls
        handler.begin = self.handle_ball_collision


        self._initialize_balls()
        # self.space.add_collision_handler(1, 1, begin=self.handle_ball_collision)  # 1 is the collision type for balls
        
        # Create boundary walls and obstacle
        self._initialize_boundaries_and_obstacle()

        self._initialize_triangle_obstacle()


    def _initialize_balls(self):
        self.balls = []
        for _ in range(NUMBER_OF_BALLS):
            x = random.randint(BALL_RADIUS, SCREEN_WIDTH - BALL_RADIUS)
            y = random.randint(BALL_RADIUS, SCREEN_HEIGHT - BALL_RADIUS)
            dx = random.randint(-150, 150)
            dy = random.randint(-150, 150)

            new_ball = Ball(x, y, dx, dy)

            self.balls.append( new_ball )

        # Now adjust the temperature for a subset of balls
        for ball in random.sample(self.balls, 10):
            ball.temperature = random.uniform(PropertiesofNature.Temperature.ambient, PropertiesofNature.Temperature.ambient * 2)

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

        for ball in self.balls:
            ball.nearby_balls.clear()

        # Check for balls in close proximity
        for i, ball_a in enumerate(self.balls):
            for ball_b in self.balls[i+1:]:  # Start from i+1 to avoid checking a pair twice
                distance = ball_a.body.position.get_distance(ball_b.body.position)
                if distance <= 2*BALL_RADIUS + 0.5:  # 0.5 is a small buffer to account for balls very close to each other
                    ball_a.nearby_balls.add(ball_b)
                    ball_b.nearby_balls.add(ball_a)

        # Compute heat transfer for balls in close proximity
        for ball in self.balls:
            for nearby_ball in ball.nearby_balls:
                ball.compute_heat_transfer(nearby_ball, delta_time)
            
            ball.update(delta_time)

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
        # # Clear all bodies and shapes from the space
        # for shape in self.space.shapes:
        #     self.space.remove(shape)
        # for body in self.space.bodies:
        #     self.space.remove(body)
        
        # self.balls = self._initialize_balls()
        # for ball in self.balls:
        #     self.space.add(ball.body, ball.shape)
        
        # # Create boundary walls and obstacle
        # self._initialize_boundaries_and_obstacle()
        self._initialize_balls()
        # self.space.add_collision_handler(1, 1, begin=self.handle_ball_collision)  # 1 is the collision type for balls
        
        # Create boundary walls and obstacle
        self._initialize_boundaries_and_obstacle()

        self._initialize_triangle_obstacle()
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.reset_simulation()




class ProfileGame(MyGame):
    def __init__(self, screen_width, screen_height):
        super().__init__(screen_width, screen_height)
        self.profiler = cProfile.Profile()

    def update(self, delta_time):
        self.profiler.enable()
        super().update(delta_time)
        self.profiler.disable()

    def on_close(self):
        self.profiler.print_stats(sort="cumulative")
        super().on_close()