import pygame
from constants import ALIVE, ZOMBIE, DEAD
from game_of_life import GameOfLife
from rules import classic_rules, zombie_rules, von_neumann_rules, respawn_rules
import time

CELL_SIZE = 15
BUTTON_HEIGHT = 40
BUTTON_WIDTH = 100
MARGIN = 10
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
UI_WIDTH = 200
GAME_WIDTH = WINDOW_WIDTH - UI_WIDTH
CELL_COLORS = {
    ALIVE: (255, 255, 255),   # blanc
    ZOMBIE: (0, 200, 0)       # vert
}

engine = None
board = None
rows = 0
cols = 0
offset_x = 0
offset_y = 0
SCROLL_SPEED = 20

pygame.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

pygame.display.set_caption("Game of Life")
clock = pygame.time.Clock()

running = True
paused = True
current_view = "game"


SPEEDS = {"Fast": 0.5, "Medium": 1, "Slow": 3}
current_speed = "Fast"
last_update = time.time()

BOARD_SIZES = {
    "Small": (53, 53),
    "Medium": (200, 200),
    "Big": (1000, 1000)
}

current_board_size = "Medium"

RULES = {
    "Classic": classic_rules,
    "Zombie": zombie_rules,
    "Von Neumann": von_neumann_rules,
    "Respawn": respawn_rules
}

current_rule = "Classic"

start_button = pygame.Rect(
    GAME_WIDTH + MARGIN,
    MARGIN,
    UI_WIDTH - 2*MARGIN,
    BUTTON_HEIGHT
)

exit_button = pygame.Rect(
    GAME_WIDTH + MARGIN,
    MARGIN*2 + BUTTON_HEIGHT,
    UI_WIDTH - 2*MARGIN,
    BUTTON_HEIGHT
)

settings_button = pygame.Rect(
    GAME_WIDTH + MARGIN,
    MARGIN*3 + BUTTON_HEIGHT*2,
    UI_WIDTH - 2*MARGIN,
    BUTTON_HEIGHT
)

speed_buttons = {
    "Fast": pygame.Rect(50, 50, BUTTON_WIDTH, BUTTON_HEIGHT),
    "Medium": pygame.Rect(50, 50 + BUTTON_HEIGHT + MARGIN, BUTTON_WIDTH, BUTTON_HEIGHT),
    "Slow": pygame.Rect(50, 50 + 2*(BUTTON_HEIGHT + MARGIN), BUTTON_WIDTH, BUTTON_HEIGHT)
}

size_buttons = {
    "Small": pygame.Rect(50, 220, BUTTON_WIDTH, BUTTON_HEIGHT),
    "Medium": pygame.Rect(50, 220 + BUTTON_HEIGHT + MARGIN, BUTTON_WIDTH, BUTTON_HEIGHT),
    "Big": pygame.Rect(50, 220 + 2*(BUTTON_HEIGHT + MARGIN), BUTTON_WIDTH, BUTTON_HEIGHT)
}

rule_buttons = {
    "Classic": pygame.Rect(50, 380, BUTTON_WIDTH, BUTTON_HEIGHT),
    "Zombie": pygame.Rect(50, 380 + BUTTON_HEIGHT + MARGIN, BUTTON_WIDTH, BUTTON_HEIGHT),
    "Von Neumann": pygame.Rect(50, 380 + 2*(BUTTON_HEIGHT + MARGIN), BUTTON_WIDTH, BUTTON_HEIGHT),
    "Respawn": pygame.Rect(50, 380 + 3*(BUTTON_HEIGHT + MARGIN), BUTTON_WIDTH, BUTTON_HEIGHT)
}

font = pygame.font.Font(None, 30)

def draw_buttons():
    # Start/Pause
    pygame.draw.rect(screen, (0, 200, 0) if paused else (200, 0, 0), start_button)
    text = font.render("Start" if paused else "Pause", True, (255, 255, 255))
    screen.blit(text, (start_button.x + 10, start_button.y + 5))

    # Exit
    pygame.draw.rect(screen, (0, 0, 200), exit_button)
    text = font.render("Exit", True, (255, 255, 255))
    screen.blit(text, (exit_button.x + 25, exit_button.y + 5))

    # Settings
    pygame.draw.rect(screen, (150, 150, 0), settings_button)
    text = font.render("Settings", True, (255, 255, 255))
    screen.blit(text, (settings_button.x + 5, settings_button.y + 5))

def draw_speed_buttons():
    for name, rect in speed_buttons.items():
        color = (0, 200, 0) if current_speed == name else (150, 150, 150)
        pygame.draw.rect(screen, color, rect)
        text = font.render(name, True, (255, 255, 255))
        screen.blit(text, (rect.x + 10, rect.y + 5))

def draw_size_buttons():
    label = font.render("Board Size", True, (255, 255, 255))
    screen.blit(label, (50, 190))

    for name, rect in size_buttons.items():
        color = (0, 200, 0) if current_board_size == name else (150, 150, 150)
        pygame.draw.rect(screen, color, rect)
        text = font.render(name, True, (255, 255, 255))
        screen.blit(text, (rect.x + 10, rect.y + 5))

def draw_rule_buttons():
    label = font.render("Rules", True, (255, 255, 255))
    screen.blit(label, (50, 350))

    for name, rect in rule_buttons.items():
        color = (0, 200, 0) if current_rule == name else (150, 150, 150)
        pygame.draw.rect(screen, color, rect)
        text = font.render(name, True, (255, 255, 255))
        screen.blit(text, (rect.x + 10, rect.y + 5))


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos):
                paused = not paused
                if engine is None:
                    width, height = BOARD_SIZES[current_board_size]
                    rules = RULES[current_rule]
                    engine = GameOfLife(width=width, height=height, rules=rules)
                    board = engine.board
                    rows = len(board)
                    cols = len(board[0])
            elif exit_button.collidepoint(event.pos):
                running = False
            elif settings_button.collidepoint(event.pos):
                current_view = "settings" if current_view == "game" else "game"
            elif current_view == "settings":
                for name, rect in speed_buttons.items():
                    if rect.collidepoint(event.pos):
                        current_speed = name
                for name, rect in size_buttons.items():
                    if rect.collidepoint(event.pos) and engine is None:
                        current_board_size = name
                for name, rect in rule_buttons.items():
                    if rect.collidepoint(event.pos) and engine is None:
                        current_rule = name
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                offset_x -= SCROLL_SPEED
            elif event.key == pygame.K_RIGHT:
                offset_x += SCROLL_SPEED
            elif event.key == pygame.K_UP:
                offset_y -= SCROLL_SPEED
            elif event.key == pygame.K_DOWN:
                offset_y += SCROLL_SPEED

    screen.fill((0, 0, 0))
    
    if board is not None:
        max_x = len(board[0]) * CELL_SIZE - GAME_WIDTH
        max_y = len(board) * CELL_SIZE - WINDOW_HEIGHT

        offset_x = max(0, min(offset_x, max_x))
        offset_y = max(0, min(offset_y, max_y))

    if current_view == "game" and board is not None:
        for i, row in enumerate(board):
            for j, cell in enumerate(row):
                if cell != DEAD:
                    color = CELL_COLORS.get(cell, (255, 0, 0))

                    x = j * CELL_SIZE - offset_x
                    y = i * CELL_SIZE - offset_y

                    if -CELL_SIZE < x < GAME_WIDTH and -CELL_SIZE < y < WINDOW_HEIGHT:
                        pygame.draw.rect(
                            screen,
                            color,
                            (x, y, CELL_SIZE, CELL_SIZE)
                        )

        if not paused:
            now = time.time()
            if now - last_update >= SPEEDS[current_speed]:
                engine.step()
                board = engine.board
                last_update = now

    elif current_view == "settings":
        screen.fill((20, 20, 20))
        draw_speed_buttons()
        draw_size_buttons()
        draw_rule_buttons()

    pygame.draw.rect(
        screen,
        (30, 30, 30),
        (GAME_WIDTH, 0, UI_WIDTH, WINDOW_HEIGHT)
    )

    draw_buttons()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
