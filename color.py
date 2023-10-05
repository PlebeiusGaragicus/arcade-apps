# Useful colors for games
SNEK_GREEN = (90, 255, 50)
SNEK_DEAD = (30, 90, 20)
BRIGHT_GREEN = (50, 255, 0)
GREEN_1 = (40, 230, 0)
GREEN_2 = (20, 210, 0)
LIGHT_GREEN = (20, 200, 0)
DARK_GREEN = (0, 100, 0)
DARK_BROWN = (101, 67, 33)
BRIGHT_GOLD = (255, 215, 0)
LIGHT_GOLD = (255, 236, 139)
DARK_RED = (139, 0, 0)
RED = (200, 20, 20)
LIGHT_RED = (255, 0, 0)
DEEP_PINK = (255, 20, 147)
BRIGHT_PINK = (255, 192, 203)
DARK_DEEP_PINK = (191, 0, 119)
CRIMSON = (220, 20, 60)
DARK_CRIMSON = (139, 0, 0) #?? never tried this one
DARK_CRIMSON2 = (100, 0, 0) #?? never tried this one
DEEP_GREY = (20, 20, 20)
DARK_GREY = (105, 105, 105)
BITCOIN_ORANGE = "#ff9416"

# TODO
# SCREEN_SIZE = (240, 240) # i want this to be dynamic... or pulled from controller

def lerp(color1, color2, t):
    """Linearly interpolate between two RGB colors.

    Args:
        color1 (Tuple[int, int, int]): The first color as an RGB tuple.
        color2 (Tuple[int, int, int]): The second color as an RGB tuple.
        t (float): The interpolation factor (0.0 = color1, 1.0 = color2).

    Returns:
        Tuple[int, int, int]: The interpolated color as an RGB tuple.
    """
    r = int(color1[0] + (color2[0] - color1[0]) * t)
    g = int(color1[1] + (color2[1] - color1[1]) * t)
    b = int(color1[2] + (color2[2] - color1[2]) * t)
    return (r, g, b)
