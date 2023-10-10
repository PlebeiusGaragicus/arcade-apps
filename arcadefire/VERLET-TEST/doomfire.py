import arcade
import random

SCREEN_WIDTH = 512
SCREEN_HEIGHT = 512
SCREEN_TITLE = "Doom Fire"

# Color palette
intensity_colors = [
    (7, 7, 7),
    (31, 7, 7),
    (47, 15, 7),
    (71, 15, 7),
    (87, 23, 7),
    (103, 31, 7),
    (119, 31, 7),
    (143, 39, 7),
    (159, 47, 7),
    (175, 63, 7),
    (191, 71, 7),
    (199, 71, 7),
    (223, 79, 7),
    (223, 87, 7),
    (223, 87, 7),
    (215, 95, 7),
    (215, 95, 7),
    (215, 103, 15),
    (207, 111, 15),
    (207, 119, 15),
    (207, 127, 15),
    (207, 135, 23),
    (199, 135, 23),
    (199, 143, 23),
    (199, 151, 31),
    (191, 159, 31),
    (191, 159, 31),
    (191, 167, 39),
    (191, 167, 39),
    (191, 175, 47),
    (183, 175, 47),
    (183, 183, 47),
    (183, 183, 55),
    (207, 207, 111),
    (223, 223, 159),
    (239, 239, 199)
]


def get_color_by_intensity(intensity):
    if 0 <= intensity < 36:
        return intensity_colors[intensity]
    return (0, 0, 0)


class DoomFire(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.pixel_size = 8
        self.fire_width = 64
        self.fire_height = 64
        self.struct_fire = [[0 for _ in range(self.fire_width)] for _ in range(self.fire_height)]

        for row in range(self.fire_width):
            for column in range(self.fire_height):
                if row + 1 < self.fire_width:
                    self.struct_fire[row][column] = 0
                else:
                    self.struct_fire[row][column] = 35

    def update(self, delta_time):
        for row in range(self.fire_width):
            for column in range(self.fire_height):
                if column + 1 < self.fire_height:
                    decay = random.randint(0, 2)
                    intensity_below = max(self.struct_fire[column + 1][row] - decay, 0)
                    if row - decay >= 0:
                        self.struct_fire[column][row - decay] = intensity_below
                    elif column - 1 >= 0:
                        self.struct_fire[column][self.fire_height - decay] = intensity_below
                    else:
                        self.struct_fire[column][row] = intensity_below

    def on_draw(self):
        arcade.start_render()
        for row in range(self.fire_width):
            for column in range(self.fire_height):
                color = get_color_by_intensity(self.struct_fire[row][column])
                arcade.draw_rectangle_filled(column * self.pixel_size + self.pixel_size / 2,
                                             row * self.pixel_size + self.pixel_size / 2,
                                             self.pixel_size,
                                             self.pixel_size,
                                             color)


if __name__ == "__main__":
    window = DoomFire()
    arcade.run()
