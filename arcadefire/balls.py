import math
import random

from arcadefire.config import BALL_RADIUS, SCREEN_WIDTH, SCREEN_HEIGHT, PropertiesofNature

import arcade
import pymunk



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

        self.nearby_balls = set()

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

    def compute_heat_transfer(self, other_ball, delta_time):
        transfer_coefficient = 0.05  # Adjust as necessary
        heat_transfer = transfer_coefficient * (self.temperature - other_ball.temperature) * delta_time
        self.temperature += heat_transfer
        other_ball.temperature -= heat_transfer  # Opposite sign because heat moves from hotter to colder ball

    def draw(self):
        self.sync_sprite()
        self.sprite.color = self.get_color_based_on_temperature()
        self.sprite.draw()
