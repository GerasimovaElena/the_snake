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

# Movement directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Background color
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Speed of the game
SPEED = 10

# Setting up the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Title of the game window
pygame.display.set_caption('The Snake')

# Setting the time
clock = pygame.time.Clock()


class GameObject:
    """
    The base class from which other game objects are inherited.
    It contains common attributes of game objects.
    """

    def __init__(self) -> None:
        """Inits GameObject."""
        self.body_color = BOARD_BACKGROUND_COLOR
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

    def draw(self, surface):
        """
        An abstract method that should determine
        how an object will appear on the screen.
        """
        raise NotImplementedError('Method not implemented!')


class Snake(GameObject):
    """The class describing the snake and its behavior."""

    def __init__(self) -> None:
        """Inits the snake."""
        super().__init__()
        self.body_color = (60, 179, 113)
        self.reset()
        self.direction = RIGHT
        self.last: Optional[Tuple[int, int]] = None
        self.next_direction: Optional[Tuple[int, int]] = None

    def update_direction(self) -> None:
        """Updates the snake's direction."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> List[Tuple[int, int]]:
        """Updates the position of the snake (coordinates of each segment)."""
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
        """Gets the position of the snake's head."""
        return self.positions[0]

    def reset(self) -> None:
        """Resets the snake."""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        screen.fill(color=BOARD_BACKGROUND_COLOR)

    def draw(self, surface):
        """Draws the snake on the screen."""
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, (60, 179, 113), rect, 1)

        # Drawing the snake's head
        head = self.positions[0]
        head_rect = pygame.Rect((head[0], head[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, (60, 179, 113), head_rect, 1)

        # Painting over the last segment
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)


class Apple(GameObject):
    """The class that describes the apple and its actions."""

    def __init__(self) -> None:
        """Inits the apple."""
        self.body_color = (250, 20, 60)
        self.position = self.randomize_position()

    def randomize_position(
            self,
            occupied_positions: Optional[List[Tuple[int, int]]] = None
    ) -> Tuple[int, int]:
        """
        The method responsible for the random appearance
        of the apple on the screen.
        """
        occupied_positions = occupied_positions or []
        available_positions = [
            (x * GRID_SIZE, y * GRID_SIZE)
            for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT)
            if (x * GRID_SIZE, y * GRID_SIZE) not in occupied_positions
        ]
        if available_positions:
            new_position = choice(available_positions)
            self.position = new_position
        else:
            # Handle case when no available positions
            pass
        return self.position

    def draw(self, surface):
        """Draws the apple on the screen."""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, (255, 160, 122), rect, 1)


def handle_keys(game_object) -> None:
    """User action processing."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN
                                         and event.key == pygame.K_ESCAPE):
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            turns = {
                (pygame.K_UP, DOWN): UP,
                (pygame.K_DOWN, UP): DOWN,
                (pygame.K_LEFT, RIGHT): LEFT,
                (pygame.K_RIGHT, LEFT): RIGHT,
            }
            for (k_key, direction) in turns:
                if event.key == k_key and game_object.direction != direction:
                    game_object.next_direction = turns.get((k_key, direction))
                    break


def main():
    """Main Game Loop."""
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
