from math import atan2, cos, sin
import arcade
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BALL_RADIUS = 15
BALL_COUNT = 30
# GRAVITY = -0.5
GRAVITY = -0.5
# TIME_STEP = 1/60
TIME_STEP = 1/10
FRICTION = 0.99

class Ball:
    def __init__(self, x, y):
        self.current_position = [x, y]
        self.previous_position = [x, y]
        self.acceleration = [0, GRAVITY]

    def apply_gravity(self):
        self.acceleration[1] = GRAVITY

    def update(self):
        for i in range(2):
            new_position = 2 * self.current_position[i] - self.previous_position[i] + self.acceleration[i] * TIME_STEP * TIME_STEP
            self.previous_position[i] = self.current_position[i]
            self.current_position[i] = new_position
            
        # Damping the motion a little to simulate friction
        velocity_x = (self.current_position[0] - self.previous_position[0])
        velocity_y = (self.current_position[1] - self.previous_position[1])
        
        self.previous_position[0] -= (1 - FRICTION) * velocity_x
        self.previous_position[1] -= (1 - FRICTION) * velocity_y

    def handle_collisions(self):
        # Horizontal collisions (left and right)
        if self.current_position[0] - BALL_RADIUS < 0:
            self.current_position[0] = BALL_RADIUS
            self.previous_position[0] = self.current_position[0] + (self.previous_position[0] - self.current_position[0])
        elif self.current_position[0] + BALL_RADIUS > SCREEN_WIDTH:
            self.current_position[0] = SCREEN_WIDTH - BALL_RADIUS
            self.previous_position[0] = self.current_position[0] + (self.previous_position[0] - self.current_position[0])

        # Vertical collisions (top and bottom)
        if self.current_position[1] - BALL_RADIUS < 0:
            self.current_position[1] = BALL_RADIUS
            self.previous_position[1] = self.current_position[1] + (self.previous_position[1] - self.current_position[1])
        elif self.current_position[1] + BALL_RADIUS > SCREEN_HEIGHT:
            self.current_position[1] = SCREEN_HEIGHT - BALL_RADIUS
            self.previous_position[1] = self.current_position[1] + (self.previous_position[1] - self.current_position[1])

    def handle_ball_collision(self, other):
        dx = self.current_position[0] - other.current_position[0]
        dy = self.current_position[1] - other.current_position[1]

        distance = (dx**2 + dy**2)**0.5

        if distance < 2 * BALL_RADIUS:
            overlap = 2 * BALL_RADIUS - distance

            # Calculate displacement required
            angle = atan2(dy, dx)
            displacement_x = overlap/2 * cos(angle)
            displacement_y = overlap/2 * sin(angle)

            # Push balls apart based on their mass (assuming equal mass here)
            self.current_position[0] += displacement_x
            self.current_position[1] += displacement_y
            other.current_position[0] -= displacement_x
            other.current_position[1] -= displacement_y

            # Reflect previous positions based on their relative velocities
            relative_velocity_x = (self.current_position[0] - self.previous_position[0]) - (other.current_position[0] - other.previous_position[0])
            relative_velocity_y = (self.current_position[1] - self.previous_position[1]) - (other.current_position[1] - other.previous_position[1])

            # Here, we're introducing elasticity. 
            # If elasticity = 1, then perfect reflection occurs.
            # If elasticity < 1, then some energy is lost in the collision.
            elasticity = 0.1
            reflection_x = relative_velocity_x * elasticity
            reflection_y = relative_velocity_y * elasticity

            self.previous_position[0] -= reflection_x
            self.previous_position[1] -= reflection_y
            other.previous_position[0] += reflection_x
            other.previous_position[1] += reflection_y




class PhysicsSimulator(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height, "Physics Simulator with Arcade")
        arcade.set_background_color(arcade.color.WHITE)
        self.ball_list = []

        for _ in range(BALL_COUNT):
            x = random.uniform(BALL_RADIUS, SCREEN_WIDTH - BALL_RADIUS)
            y = random.uniform(BALL_RADIUS, SCREEN_HEIGHT - BALL_RADIUS)
            ball = Ball(x, y)
            self.ball_list.append(ball)

    def on_draw(self):
        arcade.start_render()
        for ball in self.ball_list:
            arcade.draw_circle_filled(ball.current_position[0], ball.current_position[1], BALL_RADIUS, arcade.color.BLUE)

    def update(self, delta_time):
        for ball in self.ball_list:
            ball.apply_gravity()
            ball.update()
            ball.handle_collisions()

        # Ball-to-ball collision detection and resolution
        for i in range(len(self.ball_list)):
            for j in range(i+1, len(self.ball_list)):
                self.ball_list[i].handle_ball_collision(self.ball_list[j])

if __name__ == "__main__":
    window = PhysicsSimulator(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()
