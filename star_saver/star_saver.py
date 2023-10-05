import random
import time
from dataclasses import dataclass

from PIL import Image, ImageDraw

from seedsigner.hardware.buttons import HardwareButtonsConstants
from seedsigner.gui.components import load_image

from modules.games import BaseGameScreen
from modules.games.color import *

from .objects import Astroid, Bomb, PowerBar, PowerGem, Enemy
from .config import *


@dataclass
class Handler(BaseGameScreen):
    def setup(self):
        opaque = load_image("game/ship_tiny.png")
        alpha = opaque.split()[-1]  # get the alpha channel from the image
        # create a new image with the same size and color as the original, but with alpha set to 0 (fully transparent)
        self.ship_image = Image.new('RGBA', opaque.size, (255, 255, 255, 0))
        self.ship_image.paste(opaque, mask=alpha)  # paste the original image into the new one, using the alpha channel as a mask

        self.ship_width = self.ship_image.width
        self.ship_height = self.ship_image.height

        self.hero_x = int(self.renderer.disp.width / 2 - self.ship_image.width / 2)
        self.hero_y = int(self.renderer.disp.height * 0.80 - self.ship_image.height / 2)

        # self.power_bar = PowerBar(x=2, y=self.renderer.canvas_height-14, width=236, height=10, max_power=100)
        self.power_bar = PowerBar(x=2, y=self.renderer.canvas_height-14, width=236, height=10, max_power=100)

        self.bombs = []
        self.last_shot_time = None

        self.astroids = []
        self.powergems = []
        self.enemies = []


    def update(self):
        if self.power_bar.power == 0:
            self.alive = False
            # self.power_bar.change_power(100)

        # print(self.hero_x, self.hero_x + self.ship_width)
        # TODO - if debug mode
        # print(self.hero_y, self.hero_y + self.ship_height)

        # 10% chance
        if random.randint(0, 100) < 10:
            self.astroids.append(Astroid(random.randint(0, self.renderer.disp.width), 0, random.randint(1, 5)))

        # 2% chance
        if random.randint(0, 100) < 2:
            self.powergems.append(PowerGem(random.randint(0, self.renderer.disp.width), 0, random.randint(1, 5)))
        
        if len(self.enemies) < 2:
            if random.randint(0, 100) < 2:
                self.enemies.append(Enemy(random.randint(0, self.renderer.disp.width)))

        # if we collide with a powergem, add power
        for p in self.powergems:
            if p.x > self.hero_x and p.x < self.hero_x + self.ship_width and p.y > self.hero_y and p.y < self.hero_y + self.ship_height:
                self.power_bar.change_power(10)
                self.powergems.remove(p)
        
        hero_box = self.ship_image.getbbox()
        for e in self.enemies:
            enemy_box = e.image.getbbox()

            # Check for overlap
            # if hero_box[2] >= enemy_box[0] and hero_box[0] <= enemy_box[2] and hero_box[3] >= enemy_box[1] and hero_box[1] <= enemy_box[3]:
            #     # The bounding boxes overlap, so the images might be colliding
            #     # Check for pixel-level collision
            #     for x in range(max(hero_box[0], enemy_box[0]), min(hero_box[2], enemy_box[2])):
            #         for y in range(max(hero_box[1], enemy_box[1]), min(hero_box[3], enemy_box[3])):
            #             if self.ship_image.getpixel((x - hero_box[0], y - hero_box[1]))[3] > 0 and e.image.getpixel((x - enemy_box[0], y - enemy_box[1]))[3] > 0:
            #                 # A non-transparent pixel has been found, so the images are colliding
            #                 self.power_bar.change_power(-25)
            #                 self.enemies.remove(e)

        # # TODO: This has a bug... if the hero is wider than the enemy, then no collision is detected
        # # if we collide with an enemy, lose power
        for e in self.enemies:
            # if ((left side of ship is between left and right side of enemy) OR (right side of ship is between left and right side of enemy) AND (top of ship is between top and bottom of enemy)
            if ((self.hero_x >= e.x and self.hero_x <= e.x + e.image.width) or (self.hero_x + self.ship_width >= e.x and self.hero_x + self.ship_width <= e.x + e.image.width)) and (self.hero_y >= e.y and self.hero_y <= e.y + e.image.height):
                self.power_bar.change_power(-25)
                self.enemies.remove(e)
        
        # if an enemy hits a bomb, it loses health
        for e in self.enemies:
            for b in self.bombs:
                if b.x >= e.x and b.x <= e.x + e.image.width and b.y >= e.y and b.y <= e.y + e.image.height:
                # if e.x >= b.x and e.x + e.image.width <= b.x + b.width and e.y >= b.y:
                    e.health -= b.power
                    print("ENEMY HIT")
                    if e.health <= 0:
                        self.enemies.remove(e)
                    self.bombs.remove(b)


    def input(self, input):
        if HardwareButtonsConstants.KEY_DOWN in input:
            self.hero_y += SLOW_MOVE

        if HardwareButtonsConstants.KEY_UP in input:
            self.hero_y -= SLOW_MOVE

        if HardwareButtonsConstants.KEY_LEFT in input:
            if HardwareButtonsConstants.KEY_PRESS in input:
                self.hero_x -= FAST_MOVE
                self.power_bar.change_power(-1)
            else:
                self.hero_x -= SLOW_MOVE

        if HardwareButtonsConstants.KEY_RIGHT in input:
            if HardwareButtonsConstants.KEY_PRESS in input:
                self.hero_x += FAST_MOVE
                self.power_bar.change_power(-1)
            else:
                self.hero_x += SLOW_MOVE


        ################## RETAIN HERO ON SCREEN
        if self.hero_x < 0:
            self.hero_x = 0
        if self.hero_x > 240 - self.ship_image.width:
            self.hero_x = 240 - self.ship_image.width
        if self.hero_y < 0:
            self.hero_y = 0
        if self.hero_y > 240 - self.ship_image.height - self.power_bar.height - 4:
            self.hero_y = 240 - self.ship_image.height - self.power_bar.height - 4


        # ################## ACTION BUTTON
        # # shield
        # if HardwareButtonsConstants.KEY1 in input:
        #     # alive = False
        #     # return self.results_screen()
        #     user_quits = self.pause_screen()
        #     self.hw_inputs.block_for_all_buttons_release()
        #     if user_quits:
        #         return False
        #     # else:
        #     #     print("continue...")
        #     # return Destination(BackStackView)

        if HardwareButtonsConstants.KEY2 in input:
            # wait for cooldown
            if self.last_shot_time is None or time.monotonic() - self.last_shot_time > SHOT_COOLDOWN:
                if self.power_bar.power > LITTLE_SHOT_POWER:
                    self.score += 1
                    self.last_shot_time = time.monotonic()
                    self.bombs.append(Bomb(self.hero_x + self.ship_width / 2 + 1, self.hero_y, LITTLE_SHOT_POWER))
                    self.power_bar.change_power(-LITTLE_SHOT_POWER)

        if HardwareButtonsConstants.KEY3 in input:
            # wait for cooldown
            if self.last_shot_time is None or time.monotonic() - self.last_shot_time > SHOT_COOLDOWN:
                if self.power_bar.power > BIG_SHOT_POWER:
                    self.score += 3
                    self.last_shot_time = time.monotonic()
                    self.bombs.append(Bomb(self.hero_x + self.ship_width / 2 + 1, self.hero_y, BIG_SHOT_POWER))
                    self.power_bar.change_power(-BIG_SHOT_POWER)


    def draw(self):
        image = Image.new("RGB", (240, 240), "black")
        draw = ImageDraw.Draw(image)

        # draw.ellipse((self.hero_x - 3, self.hero_y - 3, self.hero_x + 3, self.hero_y + 3), fill=(255, 255, 255), outline=(100, 155, 55))
        
        # doesn't work... bad offsets with rest of code
        # image.paste(self.ship_image, (int(self.hero_x - self.ship_image.width / 2), int(self.hero_y - self.ship_image.height / 2)))


        for a in self.astroids:
            a.draw(draw)
            if a.update():
                self.astroids.remove(a)

        for p in self.powergems:
            p.draw(draw)
            if p.update():
                self.powergems.remove(p)
        
        for e in self.enemies:
            e.draw(image)
            if e.update():
                self.enemies.remove(e)

        for b in self.bombs:
            b.draw(draw)
            if b.update():
                self.bombs.remove(b)

        # image.paste(self.ship_image, (self.hero_x, self.hero_y))
        image.paste(self.ship_image, (int(self.hero_x), int(self.hero_y)), self.ship_image)
        self.power_bar.draw(draw)

        with self.renderer.lock:
            self.renderer.disp.ShowImage(image, 0, 0)
