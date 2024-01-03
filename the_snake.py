from random import choice
from typing import List, Optional, Tuple
import pygame

# Initializing PyGame
pygame.init()

# Constants for the size of the playing field
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Moving direction
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Background color is black
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Snake speed
SPEED = 10

# Setting up the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Title of the playing field window
pygame.display.set_caption('The Snake')

# Setting the time
clock = pygame.time.Clock()


class GameObject:
    """
    The base class from which other game objects are inherited.
    It contains common attributes of game objects.
    """

    def __init__(self):
        self.body_color = None
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

    def draw(self):
        pass


class Snake(GameObject):
    """The class describing the snake and its behavior."""

    def __init__(self):
        super().__init__()
        self.body_color = (60, 179, 113)
        self.reset()
        self.direction = RIGHT
        self.last = None
        self.next_direction = None

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> List[Tuple[int, int]]:
        head_position = self.get_head_position()
        self.last = self.positions[-1]
        new_head_position = (
            (head_position[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (head_position[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        )
        if new_head_position in self.positions:
            self.reset()
        else:
            self.positions.insert(0, new_head_position)
            if len(self.positions) > self.length:
                self.positions.pop()
        return self.positions

    def get_head_position(self) -> Tuple[int, int]:
        return self.positions[0]

    def reset(self):
        """Resets the snake"""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        screen.fill(color=BOARD_BACKGROUND_COLOR)

    def draw(self, surface):
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, (60, 179, 113), rect, 1)

        # Отрисовка головы змейки
        head = self.positions[0]
        head_rect = pygame.Rect((head[0], head[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, (60, 179, 113), head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)


class Apple(GameObject):
    """Класс, описывающий яблоко и действия c ним."""

    def __init__(self):
        self.body_color = (250, 20, 60)
        self.position = self.randomize_position()

    def randomize_position(
            self,
            occupied_positions: Optional[List[Tuple[int, int]]] = None) -> Tuple[int, int]:
        """Метод отвечающий за случайное появление яблока на экране."""
        occupied_positions = occupied_positions or []
        available_positions = [
            (x * GRID_SIZE,
             y * GRID_SIZE) for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT)
            if (x * GRID_SIZE, y * GRID_SIZE) not in occupied_positions
        ]
        if available_positions:
            new_position = choice(available_positions)
            self.position = new_position
        else:
            # handle case when no available positions
            pass
        return self.position

    # Метод draw класса Apple
    def draw(self, surface):
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, (255, 160, 122), rect, 1)


# Функция обработки действий пользователя
def handle_keys(game_object):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    # Тут нужно создать экземпляры классов
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
