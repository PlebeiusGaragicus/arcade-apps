import math
import random

from arcadefire.config import BALL_RADIUS, SCREEN_WIDTH, SCREEN_HEIGHT, PropertiesofNature, NUMBER_OF_BALLS

import arcade
import pymunk


MAX_TRANSFER_AMOUNT = 10  # In Kelvin
TRANSFER_COE = 0.01  # Adjust as necessary


def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))


class Ball:
    def __init__(self, x, y, dx, dy, radius=BALL_RADIUS, temperature = None):
        mass = 1
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        self.body = pymunk.Body(mass, inertia)
        self.body.position = x, y
        self.body.velocity = dx, dy

        # Use properties from PropertiesofNature class
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.elasticity = PropertiesofNature.Ball.elasticity
        self.shape.friction = PropertiesofNature.Ball.friction

        if temperature is None:
            r = random.random() ** 9  # r^2 will skew the distribution towards 1
            min_temperature = PropertiesofNature.Temperature.max_temperature * 0.7  # 70% of max_temperature
            self.temperature = min_temperature + r * (PropertiesofNature.Temperature.max_temperature - min_temperature)
        else:
            self.temperature = temperature

        self.shape.collision_type = 1

        # self.sprite = arcade.SpriteCircle(radius, arcade.color.GREEN)
        self.sprite = arcade.SpriteCircle(radius, self.get_color_based_on_temperature())
        self.sprite.center_x = x
        self.sprite.center_y = y

        self.nearby_balls = set()

    def sync_sprite(self):
        self.sprite.center_x = self.body.position.x
        self.sprite.center_y = self.body.position.y
        self.sprite.angle = math.degrees(self.body.angle)

    def get_color_based_on_temperature(self):
        max_temp = PropertiesofNature.Temperature.max_temperature
        ratio = self.temperature / max_temp
        if ratio <= 0.2:  # Black to Red
            return (int(clamp(255 * 5 * ratio, 0, 255)), 0, 0)
        elif ratio <= 0.4:  # Red to Orange
            return (255, int(clamp(255 * 5 * (ratio - 0.2), 0, 255)), 0)
        elif ratio <= 0.6:  # Orange to Yellow
            return (255, 255, int(clamp(255 * 5 * (ratio - 0.4), 0, 255)))
        elif ratio <= 0.8:  # Yellow to White
            return (255, 255, 255)
        else:  # White to Blue (for hotter than typical temperatures)
            return (255 - int(clamp(255 * 5 * (ratio - 0.8), 0, 255)), 255 - int(clamp(255 * 5 * (ratio - 0.8), 0, 255)), 255)

    def transfer_temperature(self, other_ball):
        temperature_difference = self.temperature - other_ball.temperature
        if abs(temperature_difference) > 5:
            transfer_amount = min(0.1 * temperature_difference, MAX_TRANSFER_AMOUNT)
            self.temperature -= transfer_amount
            other_ball.temperature += transfer_amount

    def equilibrate_with_environment(self):
        AMBIENT_TEMPERATURE = PropertiesofNature.Temperature.ambient  # Assuming this value is defined in your PropertiesofNature
        delta_temp = (AMBIENT_TEMPERATURE - self.temperature) * 0.00001  # 1% difference per frame
        self.temperature += delta_temp

    def compute_heat_transfer(self, other_ball, delta_time):
        transfer_coefficient = TRANSFER_COE  # Adjust as necessary
        heat_transfer = transfer_coefficient * (self.temperature - other_ball.temperature) * delta_time
        # self.temperature += heat_transfer
        # other_ball.temperature -= heat_transfer  # Opposite sign because heat moves from hotter to colder ball
        if self.temperature > other_ball.temperature:
            self.temperature -= abs(heat_transfer)
            other_ball.temperature += abs(heat_transfer)
        else:
            self.temperature += abs(heat_transfer)
            other_ball.temperature -= abs(heat_transfer)

    def update(self, delta_time):
        # Add this function if it doesn't already exist. This will be where all per-frame logic for the ball goes.
        self.equilibrate_with_environment()  # Ensure each ball tries to reach equilibrium with the environment over time

    def draw(self):
        self.sync_sprite()
        self.sprite.color = self.get_color_based_on_temperature()
        self.sprite.draw()

        # draw the temperature on top of each ball
        # arcade.draw_text(f"{int(self.temperature)}K", self.body.position.x - BALL_RADIUS, self.body.position.y + BALL_RADIUS, arcade.color.BLACK, 10)

        # draw the temp in the middle of each ball
        # arcade.draw_text(f"{int(self.temperature)}K", self.body.position.x - BALL_RADIUS, self.body.position.y, arcade.color.BLACK, 10)
