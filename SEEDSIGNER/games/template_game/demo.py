DEBUG = False


import random
import time
from dataclasses import dataclass

from PIL import Image, ImageDraw

from seedsigner.hardware.buttons import HardwareButtonsConstants
# from seedsigner.gui.components import GUIConstants, FontAwesomeIconConstants
from seedsigner.gui.components import load_image
# from seedsigner.gui.screens.game_screens import BaseGameScreen

from modules.games import BaseGameScreen
from modules.games.fonts import FontAwesomeIcons
# from helpers import lerp
# from seedsigner.gui.screens.game_screens import lerp



MOVEMENT_SPEED = 6


@dataclass
class Handler(BaseGameScreen):
    display_name: str = "Demo"
    font_icon: FontAwesomeIcons = FontAwesomeIcons.LOCATION_CROSSHAIRS    
    intro_image_filename: str = None # TODO should be Path()???

    # TODO - DO I need thesee...???
    def __post_init__(self):
        super().__post_init__()


    def setup(self):
        opaque = load_image("game/dot.png")
        alpha = opaque.split()[-1]  # get the alpha channel from the image
        # create a new image with the same size and color as the original, but with alpha set to 0 (fully transparent)
        self.player_image = Image.new('RGBA', opaque.size, (255, 255, 255, 0))
        self.player_image.paste(opaque, mask=alpha)  # paste the original image into the new one, using the alpha channel as a mask

        self.player_x = int(self.renderer.disp.width / 2 - self.player_image.width / 2)
        self.player_y = int(self.renderer.disp.height * 0.80 - self.player_image.height / 2)


    def update(self):
        pass


    def input(self, input):

        if HardwareButtonsConstants.KEY_DOWN in input:
            self.player_y += MOVEMENT_SPEED

        if HardwareButtonsConstants.KEY_UP in input:
            self.player_y -= MOVEMENT_SPEED

        if HardwareButtonsConstants.KEY_LEFT in input:
            self.player_x -= MOVEMENT_SPEED

        if HardwareButtonsConstants.KEY_RIGHT in input:
            self.player_x += MOVEMENT_SPEED

        if self.player_x < 0:
            self.player_x = 0
        if self.player_x > self.renderer.canvas_height - self.player_image.width:
            self.player_x = self.renderer.canvas_height - self.player_image.width
        if self.player_y < 0:
            self.player_y = 0
        if self.player_y > self.renderer.canvas_width - self.player_image.height:
            self.player_y = self.renderer.canvas_width - self.player_image.height


    def draw(self):
        image = Image.new("RGB", (240, 240), "black")

        image.paste(self.player_image, (int(self.player_x), int(self.player_y)), self.player_image)

        with self.renderer.lock:
            self.renderer.disp.ShowImage(image, 0, 0)
