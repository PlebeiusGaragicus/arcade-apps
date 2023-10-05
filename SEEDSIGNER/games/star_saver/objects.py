from dataclasses import dataclass

from PIL import Image
from seedsigner.gui.components import load_image

from modules.games.color import *

from .config import *

class Astroid:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

    def draw(self, draw):
        draw.ellipse((self.x, self.y, self.x + self.size, self.y + self.size), fill=DARK_BROWN)

    def update(self):
        self.y += self.size
        if self.y > 240: # off the bottom of the screen
            return True
        return False



class Bomb:
    def __init__(self, x, y, power):
        self.x = x
        self.y = y
        self.power = power
        if self.power == LITTLE_SHOT_POWER:
            self.width, self.height = (2, 10)
        else:
            self.width, self.height = (4, 11)

    def draw(self, draw):
        draw.rectangle((self.x, self.y, self.x + self.width, self.y + self.height), fill=DEEP_PINK if self.power == LITTLE_SHOT_POWER else BRIGHT_GOLD)

    def update(self):
        self.y -= SHOT_SPEED
        if self.y < -10: # off the top of the screen
            return True
        return False



@dataclass
class PowerBar:
    x: int
    y: int
    width: int
    height: int
    max_power: int
    _power: int = 98

    def draw(self, draw):

        # Calculate the interpolation factor based on the power level
        t = self.power / self.max_power

        # Interpolate between the two colors using the lerp function
        color = lerp(DEEP_PINK, BRIGHT_GOLD, t)
        outline_color = lerp(DARK_DEEP_PINK, LIGHT_GOLD, t)

        # Draw the three rectangles with the interpolated color
        draw.rectangle((self.x, self.y, self.x + self.width, self.y + self.height), fill=color, outline=outline_color)
        draw.rectangle((self.x + 2, self.y + 2, self.x + self.width - 2, self.y + self.height - 2), fill=(0, 0, 0), outline=(0, 0, 0))
        draw.rectangle((self.x + 2, self.y + 2, self.x + 2 + (self.width - 4) * (self.power / self.max_power), self.y + self.height - 2), fill=color, outline=BRIGHT_GOLD)

    @property
    def power(self):
        return self._power

    @power.setter
    def power(self, value):
        if value < 0:
            self._power = 0
        elif value > self.max_power:
            self._power = self.max_power
        else:
            self._power = value
    
    def change_power(self, delta):
        self.power += delta



class PowerGem:
    def __init__(self, x, y, power):
        self.x = x
        self.y = y
        self.power = power

    def draw(self, draw):
        width, height = (4, 4)

        draw.ellipse((self.x, self.y, self.x + width, self.y + height), fill=BRIGHT_PINK)


    def update(self):
        self.y += 5
        if self.y > 240: # off the bottom of the screen
            return True
        return False

# class Enemy:
#     def __init__(self, x):
#         self.opaque = load_image("game/enemy.png")
#         alpha = self.opaque.split()[-1]  # get the alpha channel from the image
#         # create a new image with the same size and color as the original, but with alpha set to 0 (fully transparent)
#         self.image = Image.new('RGBA', self.opaque.size, (255, 255, 255, 0))
#         self.image.paste(self.opaque, mask=alpha)  # paste the original image into the new one, using the alpha channel as a mask
#         self.x = x
#         self.y = -self.image.height
#         self.health = LITTLE_SHOT_POWER * 3.1

#     def draw(self, image):
#         image.paste(image, (int(self.x), int(self.y)), self.image)

class Enemy:
    def __init__(self, x):
        self.opaque = load_image("game/enemy.png")
        alpha = self.opaque.split()[-1]  # get the alpha channel from the image
        # create a new image with the same size and color as the original, but with alpha set to 0 (fully transparent)
        self.image = Image.new('RGBA', self.opaque.size, (255, 255, 255, 0))
        self.image.paste(self.opaque, mask=alpha)  # paste the original image into the new one, using the alpha channel as a mask
        self.x = x
        self.y = -self.image.height
        self.health = LITTLE_SHOT_POWER * 3.1

    def draw(self, image):
        image.paste(self.image, (int(self.x), int(self.y)), self.image)

    def update(self):
        self.y += 5
        if self.y > 240: # off the bottom of the screen
            return True
        return False
