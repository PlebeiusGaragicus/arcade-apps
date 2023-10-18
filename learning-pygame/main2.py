import pygame
import random

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Screen dimensions
WIDTH = 640
HEIGHT = 480
CELL_SIZE = 20
TOP_SPEED = 12

# Snake dimensions
MAX_RADIUS = 10
MIN_RADIUS = 5

# Directions
# LEFT = (-2, 0)
# RIGHT = (MOVE_DISTANCE, 0)
# UP = (0, -MOVE_DISTANCE)
# DOWN = (0, MOVE_DISTANCE)

class Snake:
    def __init__(self):
        self.body = [(5, 5), (4, 5), (3, 5)]
        self.speed_x = 1
        self.speed_y = 0

    def change_speed_cap(self, x_delta: int = None, y_delta: int = None) -> None:
        if x_delta is not None:
            if abs(self.speed_x) > TOP_SPEED:
                self.speed_x = TOP_SPEED if self.speed_x > 0 else -TOP_SPEED
                if self.speed_y != 0:
                    self.speed_y -= 1 if self.speed_y > 0 else -1
            else:
                self.speed_x += x_delta

        if y_delta is not None:
            if abs(self.speed_y) > TOP_SPEED:
                self.speed_y = TOP_SPEED if self.speed_y > 0 else -TOP_SPEED
                if self.speed_x != 0:
                    self.speed_x -= 1 if self.speed_x > 0 else -1
            else:
                self.speed_y += y_delta

    def move(self):
        head = self.body[0]
        new_head = (head[0] + self.speed_x, head[1] + self.speed_y)
        self.body = [new_head] + self.body[:-1]

    def grow(self):
        self.body.append(self.body[-1])

    def collides_with_itself(self):
        return self.body[0] in self.body[1:]

def draw_snake(screen, snake):
    for idx, segment in enumerate(snake.body):
        radius = MAX_RADIUS - (MAX_RADIUS - MIN_RADIUS) * (idx / len(snake.body))
        pygame.draw.circle(screen, GREEN, (int(segment[0]), int(segment[1])), int(radius))

def draw_food(screen, food_position):
    pygame.draw.rect(screen, RED, (food_position[0], food_position[1], CELL_SIZE, CELL_SIZE))

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Snake Game')

    snake = Snake()
    food_position = (random.randint(0, WIDTH - CELL_SIZE), random.randint(0, HEIGHT - CELL_SIZE))
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    snake.change_speed_cap(x_delta=-1)
                elif event.key == pygame.K_RIGHT:
                    snake.change_speed_cap(x_delta=1)
                elif event.key == pygame.K_UP:
                    snake.change_speed_cap(y_delta=-1)
                elif event.key == pygame.K_DOWN:
                    snake.change_speed_cap(y_delta=1)

        snake.move()

        if snake.collides_with_itself():
            running = False

        # Check if head collides with food
        head_rect = pygame.Rect(snake.body[0][0] - MAX_RADIUS, snake.body[0][1] - MAX_RADIUS, 2 * MAX_RADIUS, 2 * MAX_RADIUS)
        food_rect = pygame.Rect(food_position[0], food_position[1], CELL_SIZE, CELL_SIZE)
        if head_rect.colliderect(food_rect):
            snake.grow()
            food_position = (random.randint(0, WIDTH - CELL_SIZE), random.randint(0, HEIGHT - CELL_SIZE))

        screen.fill(WHITE)
        draw_snake(screen, snake)
        draw_food(screen, food_position)
        pygame.display.flip()
        clock.tick(10)

    pygame.quit()

if __name__ == '__main__':
    main()
