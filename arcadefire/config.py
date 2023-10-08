import math
import random
from dataclasses import dataclass

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
NUMBER_OF_BALLS = 100
BALL_RADIUS = 4


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
        min_temperature: float = 0.0
