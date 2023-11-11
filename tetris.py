import pygame
import random
import sys

# Constants
WIDTH, HEIGHT = 10, 20
GRID_SIZE = 30
WHITE, BLACK = (255, 255, 255), (0, 0, 0)

SHAPES = [
    ([[1, 1, 1, 1]], (255, 0, 0)),    # I
    ([[1, 1, 1],
      [1, 0, 0]], (0, 255, 0)),      # S
    ([[1, 1, 1],
      [0, 0, 1]], (0, 0, 255)),      # J
    ([[1, 1, 1],
      [0, 1, 0]], (255, 255, 0)),    # L
    ([[1, 1],
      [1, 1]], (128, 0, 128)),       # O
    ([[1, 1, 0],
      [0, 1, 1]], (255, 165, 0)),    # Z
    ([[0, 1, 1],
      [1, 1, 0]], (255, 255, 255))   # T
]

# Function to initialize the game
def initialize_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH * GRID_SIZE, HEIGHT * GRID_SIZE))
    pygame.display.set_caption("Pytris")
    clock = pygame.time.Clock()
    return screen, clock

# Function to create a new tetromino
def new_tetromino():
    shape, color = random.choice(SHAPES)
    return shape, color, [WIDTH // 2 - len(shape[0]) // 2, 0]

# Function to draw a tetromino on the screen
def draw_tetromino(screen, tetromino, position, color):
    for i, row in enumerate(tetromino):
        for j, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, color, (j * GRID_SIZE + position[0] * GRID_SIZE,
                                                 i * GRID_SIZE + position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

# Function to merge the current tetromino into the grid
def merge_tetromino(grid, tetromino, position):
    for i, row in enumerate(tetromino):
        for j, cell in enumerate(row):
            if cell:
                x, y = j + position[0], i + position[1]
                grid[y][x] = 1

# Function to check for collisions
def collision(grid, tetromino, position):
    for i, row in enumerate(tetromino):
        for j, cell in enumerate(row):
            if cell:
                x, y = j + position[0], i + position[1]
                if x < 0 or x >= WIDTH or y >= HEIGHT:
                    return True
                if y >= 0 and grid[y][x] == 1:
                    return True
    return False

# Function to remove completed lines
def remove_lines(grid):
    lines_to_remove = [i for i, row in enumerate(grid) if all(row)]
    for i in lines_to_remove:
        del grid[i]
        grid.insert(0, [0] * WIDTH)
    return len(lines_to_remove)

# Main function
def main():
    screen, clock = initialize_game()
    grid = [[0] * WIDTH for _ in range(HEIGHT)]
    fall_time = 0
    fall_speed = 500  # in milliseconds
    round_seed = 0

    while True:
        random.seed(round_seed)
        current_tetromino, tetromino_color, tetromino_position = new_tetromino()
        fall_time = 0
        round_seed += 1

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        new_position = [tetromino_position[0] - 1, tetromino_position[1]]
                        if not collision(grid, current_tetromino, new_position):
                            tetromino_position = new_position

                    elif event.key == pygame.K_RIGHT:
                        new_position = [tetromino_position[0] + 1, tetromino_position[1]]
                        if not collision(grid, current_tetromino, new_position):
                            tetromino_position = new_position

                    elif event.key == pygame.K_DOWN:
                        new_position = [tetromino_position[0], tetromino_position[1] + 1]
                        if not collision(grid, current_tetromino, new_position):
                            tetromino_position = new_position

                    elif event.key == pygame.K_UP:
                        # Rotate the tetromino
                        rotated_tetromino = list(zip(*reversed(current_tetromino)))
                        if not collision(grid, rotated_tetromino, tetromino_position):
                            current_tetromino = rotated_tetromino

                    elif event.key == pygame.K_BACKSPACE:
                        # Reset the game
                        grid = [[0] * WIDTH for _ in range(HEIGHT)]
                        fall_time = 0
                        round_seed = 0
                        break

            if pygame.K_BACKSPACE in [event.key for event in pygame.event.get() if event.type == pygame.KEYDOWN]:
                break

            current_time = pygame.time.get_ticks()
            if current_time - fall_time > fall_speed:
                new_position = [tetromino_position[0], tetromino_position[1] + 1]
                if not collision(grid, current_tetromino, new_position):
                    tetromino_position = new_position
                else:
                    merge_tetromino(grid, current_tetromino, tetromino_position)
                    lines_removed = remove_lines(grid)
                    print("Lines Removed:", lines_removed)
                    break

                fall_time = current_time

            screen.fill(BLACK)
            draw_tetromino(screen, current_tetromino, tetromino_position, tetromino_color)

            for i, row in enumerate(grid):
                for j, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(screen, WHITE, (j * GRID_SIZE, i * GRID_SIZE, GRID_SIZE, GRID_SIZE))

            pygame.display.flip()
            clock.tick(30)  # Adjust the frames per second (FPS) as needed

if __name__ == "__main__":
    main()