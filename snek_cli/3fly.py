import random
from blessed import Terminal
import time

term = Terminal()

# Constants
SNAKE_LENGTH = 5
SPEED = 0.1
HEAD_CHAR = '*'
BODY_CHAR = '#'
HEAD_COLOR = term.red_on_black
BODY_COLOR = term.brown_on_black
FOOD_CHAR = '@'
FOOD_COLOR = term.black_on_green
FLY_CHAR = 'F'
FLY_COLOR = term.yellow_on_black

# Border dimensions
BORDER_WIDTH = term.width // 2 - 4
BORDER_HEIGHT = term.height - 4

# Initial position
x, y = BORDER_WIDTH // 2 + 2, BORDER_HEIGHT // 2 + 2

# Initial snake
snake = [(x, y + i) for i in range(SNAKE_LENGTH)]

# Initial food position
food = (random.randint(3, BORDER_WIDTH - 2), random.randint(3, BORDER_HEIGHT - 2))

# Initial fly position
fly = (random.randint(3, BORDER_WIDTH - 2), random.randint(3, BORDER_HEIGHT - 2))

with term.cbreak(), term.hidden_cursor():
    # Clear the screen
    print(term.home + term.clear)

    # Draw the border
    for bx in range(2, BORDER_WIDTH + 2):
        for by in range(2, BORDER_HEIGHT + 2):
            if bx in {2, BORDER_WIDTH + 1} or by in {2, BORDER_HEIGHT + 1}:
                print(term.move_xy(bx * 2, by) + term.black_on_white('  '))

    dx, dy = 0, -1  # Initial direction: Up

    # Event loop
    while True:
        # Draw the snake
        for index, (sx, sy) in enumerate(snake):
            if index == 0:
                print(term.move_xy(sx * 2, sy) + HEAD_COLOR(HEAD_CHAR * 2))
            else:
                print(term.move_xy(sx * 2, sy) + BODY_COLOR(BODY_CHAR * 2))

        # Draw the food
        print(term.move_xy(food[0] * 2, food[1]) + FOOD_COLOR(FOOD_CHAR * 2))

        # Clear the previous fly position
        print(term.move_xy(fly[0] * 2, fly[1]) + '  ')

        # Move the fly
        new_fly = fly
        while new_fly in snake:
            fly_dir = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
            new_fly = (fly[0] + fly_dir[0], fly[1] + fly_dir[1])
        fly = new_fly

        # Check if the fly collided with the border
        if fly[0] in {2, BORDER_WIDTH + 1} or fly[1] in {2, BORDER_HEIGHT + 1}:
            fly_dir = (-fly_dir[0], -fly_dir[1])
            fly = (fly[0] + fly_dir[0], fly[1] + fly_dir[1])

        # Check if the snake ate the fly
        if (snake[0][0], snake[0][1]) == fly:
            # Generate new fly
            new_fly = (random.randint(3, BORDER_WIDTH - 2), random.randint(3, BORDER_HEIGHT - 2))
            while new_fly in snake:
                new_fly = (random.randint(3, BORDER_WIDTH - 2), random.randint(3, BORDER_HEIGHT - 2))
            fly = new_fly
            # Grow the snake by 2
            snake.extend([snake[-1]] * 2)

        # Draw the fly at the new position
        print(term.move_xy(fly[0] * 2, fly[1]) + FLY_COLOR(FLY_CHAR * 2))

        # Check for key press
        key = term.inkey(timeout=SPEED)
        if key.code == term.KEY_UP and dy == 0:
            dx, dy = 0, -1
        elif key.code == term.KEY_DOWN and dy == 0:
            dx, dy = 0, 1
        elif key.code == term.KEY_LEFT and dx == 0:
            dx, dy = -1, 0
        elif key.code == term.KEY_RIGHT and dx == 0:
            dx, dy = 1, 0
        elif key.lower() == 'q':
            break

        # Clear the last segment of the snake
        if len(snake) > 1:
            print(term.move_xy(snake[-1][0] * 2, snake[-1][1]) + '  ')

        # Move the snake
        x, y = snake[0][0] + dx, snake[0][1] + dy
        snake.insert(0, (x, y))

        # Check if the snake collided with the border
        if x in {2, BORDER_WIDTH + 1} or y in {2, BORDER_HEIGHT + 1}:
            print(term.move_xy(term.width // 2, term.height // 2) + term.red_on_black('Game Over'))
            time.sleep(2)
            break

        # Check if the snake collided with itself
        if (x, y) in snake[1:]:
            print(term.move_xy(term.width // 2, term.height // 2) + term.red_on_black('Game Over'))
            time.sleep(2)
            break
