# Tested in Pydroid with BlueStacks5

import pygame
import random
import sys, os

pygame.init()
screen_info = pygame.display.Info()

# Constants
if screen_info.current_w < screen_info.current_h:
	WIDTH, HEIGHT = round(screen_info.current_w / 60), round(screen_info.current_h / 30)
else:
	WIDTH, HEIGHT = round(screen_info.current_h / 60), round(screen_info.current_h / 30)
GRID_SIZE = 30
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
score = 0
lost = 0
lines_removed2 = 0

SHAPES = [
    ([[1, 1, 1, 1]]),   # I
    ([[1, 1, 1],
      [1, 0, 0]]),      # S
    ([[1, 1, 1],
      [0, 0, 1]]),      # J
    ([[1, 1, 1],
      [0, 1, 0]]),      # L
    ([[1, 1],
      [1, 1]]),         # O
    ([[1, 1, 0],
      [0, 1, 1]]),      # Z
    ([[0, 1, 1],
      [1, 1, 0]])       # T
]

# Function to initialize the game
def initialize_game():
    pygame.init()
    screen_info = pygame.display.Info()
    screen = pygame.display.set_mode((WIDTH * GRID_SIZE, HEIGHT * GRID_SIZE))
    pygame.display.set_caption("Pytris")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)  # Font for displaying text
    return screen, clock, font

# Function to create a new tetromino with a random color
def new_tetromino():
    shape = random.choice(SHAPES)
    color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
    return shape, color, [WIDTH // 2 - len(shape[0]) // 2, 0]

# Function to draw a tetromino on the screen
def draw_tetromino(screen, tetromino, position, color):
    for i, row in enumerate(tetromino):
        for j, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, color, (j * GRID_SIZE + position[0] * GRID_SIZE,
                                                 i * GRID_SIZE + position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

# Function to merge the current tetromino into the grid
def merge_tetromino(grid, tetromino, position, color):
    for i, row in enumerate(tetromino):
        for j, cell in enumerate(row):
            if cell:
                x, y = j + position[0], i + position[1]
                grid[y][x] = (1, color)

# Function to check for collisions
def collision(grid, tetromino, position):
    for i, row in enumerate(tetromino):
        for j, cell in enumerate(row):
            if cell:
                x, y = j + position[0], i + position[1]
                if x < 0 or x >= WIDTH or y >= HEIGHT:
                    return True
                if y >= 0 and grid[y][x][0] == 1:
                    return True
    return False

# Function to remove completed lines
def remove_lines(grid, lines_removed2, fall_speed):
    lines_to_remove = [i for i, row in enumerate(grid) if all(cell[0] for cell in row)]

    for i in reversed(lines_to_remove):
        del grid[i]
        grid.insert(0, [(0, BLACK)] * WIDTH)  # Fill the row with tuples (0, BLACK)

    lines_removed2 += len(lines_to_remove)
    fall_speed = 500 - (lines_removed2 * 25 - (lines_removed2 * 3))

    return lines_removed2, fall_speed

# Function to determine the color based on the level
def get_level_color(level):
    # todo: actually make this generate a color
    r = 255
    g = 0
    b = 255
    return(r,g,b)

# Function to display text on the screen
def display_text(screen, font, text, color, position):
    text_surface = font.render(text, True, color)
    text_width, text_height = text_surface.get_size()
    position_x = position[0] - text_width // 2
    screen.blit(text_surface, (position_x, position[1]))

# Main function
def main(lost=lost, lines_removed2=lines_removed2):
    screen, clock, font = initialize_game()
    grid = [[(0, BLACK)] * WIDTH for _ in range(HEIGHT)]  # Initialize with tuples (0, BLACK)
    fall_time = 0
    fall_speed = 500  # in milliseconds
    round_seed = random.randint(0, 9999)

    while True:
        if lost == 0:
            random.seed(round_seed)
            current_tetromino, tetromino_color, tetromino_position = new_tetromino()
            fall_time = 0
            old_fall_time = 0
            round_seed += 1
            lost = 0
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            new_position = [tetromino_position[0] - 1, tetromino_position[1]]
                            if not collision(grid, current_tetromino, new_position):
                                tetromino_position = new_position
                        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            new_position = [tetromino_position[0] + 1, tetromino_position[1]]
                            if not collision(grid, current_tetromino, new_position):
                                tetromino_position = new_position
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            new_position = [tetromino_position[0], tetromino_position[1] + 1]
                            if not collision(grid, current_tetromino, new_position):
                                tetromino_position = new_position
                        elif event.key == pygame.K_UP or event.key == pygame.K_w:
                            # Rotate the tetromino
                            rotated_tetromino = list(zip(*reversed(current_tetromino)))
                            if not collision(grid, rotated_tetromino, tetromino_position):
                                current_tetromino = rotated_tetromino
                        elif event.key == pygame.K_BACKSPACE:
                            # Stop the game
                            exit()
                        elif event.key == pygame.K_RETURN:
                            lines_removed2 = 0
                            lost = 0
                            main()

                current_time = pygame.time.get_ticks()
                if current_time - fall_time > fall_speed:
                    new_position = [tetromino_position[0], tetromino_position[1] + 1]
                    if not collision(grid, current_tetromino, new_position):
                        tetromino_position = new_position
                    else:
                        merge_tetromino(grid, current_tetromino, tetromino_position, tetromino_color)  # Pass color to merge_tetromino
                        lines_removed2, fall_speed = remove_lines(grid, lines_removed2, fall_speed)
                        break
                    old_fall_time = fall_time

                    fall_time = current_time
                if fall_time == 1:
                    lost = 0

                screen.fill(BLACK)
                draw_tetromino(screen, current_tetromino, tetromino_position, tetromino_color)

                for i, row in enumerate(grid):
                    for j, (value, color) in enumerate(row):
                        if value:
                            pygame.draw.rect(screen, color, (j * GRID_SIZE, i * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                level_color = get_level_color(lines_removed2)
                display_text(screen, font, f"Score: {lines_removed2}", level_color, (WIDTH * GRID_SIZE // 2, HEIGHT))
                pygame.display.flip()
                clock.tick(30)  # Adjust the frames per second (FPS) as needed
            if old_fall_time == 0:
                lost = 1
        else:
            screen.fill(BLACK)
            level_color = get_level_color(lines_removed2)
            display_text(screen, font, f"Score: {lines_removed2}", level_color, (WIDTH * GRID_SIZE // 2, HEIGHT * GRID_SIZE // 2 - 20))
            display_text(screen, font, "Press Enter to Restart", WHITE, (WIDTH * GRID_SIZE // 2, HEIGHT * GRID_SIZE // 2 + 20))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    lines_removed2 = 0
                    lost = 0
                    main()  # Restart the game

if __name__ == "__main__":
    main()
