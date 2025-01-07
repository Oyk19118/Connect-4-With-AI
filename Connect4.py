import numpy as np
import pygame
import sys
import random

# Define new colors
GRID_COLOR = (50, 50, 150)
BACKGROUND_COLOR = (10, 10, 30)
PLAYER1_COLOR = (200, 0, 50)
PLAYER2_COLOR = (250, 200, 0)
EMPTY_COLOR = (30, 30, 30)
BUTTON_COLOR = (0, 200, 100)
BUTTON_TEXT_COLOR = (255, 255, 255)
TEXT_COLOR = (255, 255, 255)

# Grid dimensions
GRID_ROWS = 6
GRID_COLUMNS = 7

# Piece definitions
PLAYER1 = 0
PLAYER2 = 1
EMPTY_SLOT = 0
PLAYER1_PIECE = 1
PLAYER2_PIECE = 2

# Winning length
WIN_LENGTH = 4

# Pygame settings
CELL_SIZE = 100
GRID_WIDTH = GRID_COLUMNS * CELL_SIZE
GRID_HEIGHT = GRID_ROWS * CELL_SIZE
SCREEN_HEIGHT = GRID_HEIGHT + CELL_SIZE
SCREEN_WIDTH = GRID_WIDTH
PIECE_RADIUS = CELL_SIZE // 2 - 10  # Slightly smaller than half the cell size

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Connect 4")
font = pygame.font.SysFont("monospace", 50)
button_font = pygame.font.SysFont("monospace", 30)


def initialize_grid():
    return np.zeros((GRID_ROWS, GRID_COLUMNS))


def place_piece(grid, row, col, piece):
    grid[row][col] = piece


def is_column_available(grid, col):
    return grid[GRID_ROWS - 1][col] == EMPTY_SLOT


def get_next_open_row(grid, col):
    for r in range(GRID_ROWS):
        if grid[r][col] == EMPTY_SLOT:
            return r


def check_win(grid, piece):
    # Horizontal
    for col in range(GRID_COLUMNS - 3):
        for row in range(GRID_ROWS):
            if all(grid[row][col + i] == piece for i in range(WIN_LENGTH)):
                return True

    # Vertical
    for col in range(GRID_COLUMNS):
        for row in range(GRID_ROWS - 3):
            if all(grid[row + i][col] == piece for i in range(WIN_LENGTH)):
                return True

    # Diagonals
    for col in range(GRID_COLUMNS - 3):
        for row in range(GRID_ROWS - 3):
            if all(grid[row + i][col + i] == piece for i in range(WIN_LENGTH)):
                return True

    for col in range(GRID_COLUMNS - 3):
        for row in range(3, GRID_ROWS):
            if all(grid[row - i][col + i] == piece for i in range(WIN_LENGTH)):
                return True

    return False


def draw_grid(grid, screen):
    screen.fill(BACKGROUND_COLOR)
    for col in range(GRID_COLUMNS):
        for row in range(GRID_ROWS):
            pygame.draw.rect(screen, GRID_COLOR, (col * CELL_SIZE, row * CELL_SIZE + CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.circle(screen, EMPTY_COLOR, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE + CELL_SIZE // 2), PIECE_RADIUS)
    for col in range(GRID_COLUMNS):
        for row in range(GRID_ROWS):
            if grid[row][col] == PLAYER1_PIECE:
                pygame.draw.circle(screen, PLAYER1_COLOR, (col * CELL_SIZE + CELL_SIZE // 2, SCREEN_HEIGHT - (row * CELL_SIZE + CELL_SIZE // 2)), PIECE_RADIUS)
            elif grid[row][col] == PLAYER2_PIECE:
                pygame.draw.circle(screen, PLAYER2_COLOR, (col * CELL_SIZE + CELL_SIZE // 2, SCREEN_HEIGHT - (row * CELL_SIZE + CELL_SIZE // 2)), PIECE_RADIUS)
    pygame.display.update()


def draw_winner_text(winner, screen):
    # Draw "Player X Wins!" text
    winner_text = f"Player {winner} Wins!"
    text_surface = font.render(winner_text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(text_surface, text_rect)

    # Draw restart button
    pygame.draw.rect(screen, BUTTON_COLOR, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50))
    button_text = button_font.render("Restart", True, BUTTON_TEXT_COLOR)
    button_rect = button_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 25))
    screen.blit(button_text, button_rect)
    pygame.display.update()


def restart_game():
    global grid, game_over, turn
    grid = initialize_grid()
    game_over = False
    turn = random.randint(PLAYER1, PLAYER2)
    draw_grid(grid, screen)


grid = initialize_grid()
game_over = False
turn = random.randint(PLAYER1, PLAYER2)

draw_grid(grid, screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                # Check if restart button is clicked
                if (SCREEN_WIDTH // 2 - 100 <= mouse_x <= SCREEN_WIDTH // 2 + 100) and (SCREEN_HEIGHT // 2 <= mouse_y <= SCREEN_HEIGHT // 2 + 50):
                    restart_game()

        if not game_over:
            if turn == PLAYER1 and event.type == pygame.MOUSEBUTTONDOWN:
                col = event.pos[0] // CELL_SIZE
                if is_column_available(grid, col):
                    row = get_next_open_row(grid, col)
                    place_piece(grid, row, col, PLAYER1_PIECE)
                    if check_win(grid, PLAYER1_PIECE):
                        print("Player 1 wins!")
                        game_over = True
                        draw_winner_text(1, screen)
                    turn = PLAYER2
                    draw_grid(grid, screen)

            elif turn == PLAYER2 and not game_over:
                col = random.choice([c for c in range(GRID_COLUMNS) if is_column_available(grid, c)])
                row = get_next_open_row(grid, col)
                place_piece(grid, row, col, PLAYER2_PIECE)
                if check_win(grid, PLAYER2_PIECE):
                    print("Player 2 wins!")
                    game_over = True
                    draw_winner_text(2, screen)
                turn = PLAYER1
                draw_grid(grid, screen)