import pygame
from config import Config
from game_of_life import GameOfLife
from rules import classic_rules, zombie_rules, von_neumann_rules, respawn_rules
import time


cell_size = float(Config.CELL_SIZE)
rows = 0
cols = 0
engine = None
board = None
offset_x = 0
offset_y = 0

pygame.init()

screen = pygame.display.set_mode((Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT))

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

BOARD_FILES = {
    "Blinker": "board_file/blinker.json",
    "Pulsar": "board_file/pulsar.json",
    "LWS": "board_file/lws.json"
}

current_file = None

start_button = pygame.Rect(
    Config.GAME_WIDTH + Config.MARGIN,
    Config.MARGIN,
    Config.UI_WIDTH - 2*Config.MARGIN,
    Config.BUTTON_HEIGHT
)

settings_button = pygame.Rect(
    Config.GAME_WIDTH + Config.MARGIN,
    Config.MARGIN*2 + Config.BUTTON_HEIGHT,
    Config.UI_WIDTH - 2*Config.MARGIN,
    Config.BUTTON_HEIGHT
)

reset_button = pygame.Rect(
    Config.GAME_WIDTH + Config.MARGIN,
    Config.MARGIN*3 + Config.BUTTON_HEIGHT*2,
    Config.UI_WIDTH - 2*Config.MARGIN,
    Config.BUTTON_HEIGHT
)

exit_button = pygame.Rect(
    Config.GAME_WIDTH + Config.MARGIN,
    Config.MARGIN*4 + Config.BUTTON_HEIGHT*3,
    Config.UI_WIDTH - 2*Config.MARGIN,
    Config.BUTTON_HEIGHT
)

def create_horizontal_buttons(labels, start_y):
    buttons = {}
    start_x = 50
    spacing_x = Config.BUTTON_WIDTH + Config.MARGIN

    for i, name in enumerate(labels):
        x = start_x + i * spacing_x
        buttons[name] = pygame.Rect(x, start_y, Config.BUTTON_WIDTH, Config.BUTTON_HEIGHT)

    return buttons

speed_buttons = create_horizontal_buttons(
    ["Fast", "Medium", "Slow"],
    start_y=60
)

size_buttons = create_horizontal_buttons(
    ["Small", "Medium", "Big"],
    start_y=160
)

rule_buttons = create_horizontal_buttons(
    ["Classic", "Zombie", "Von Neumann", "Respawn"],
    start_y=260
)

file_buttons = create_horizontal_buttons(
    ["Blinker", "Pulsar", "LWS"],
    start_y=360
)

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

    # Reset
    pygame.draw.rect(screen, (200, 100, 0), reset_button)
    text = font.render("Reset", True, (255, 255, 255))
    screen.blit(text, (reset_button.x + 15, reset_button.y + 5))

def draw_speed_buttons():
    for name, rect in speed_buttons.items():
        color = (0, 200, 0) if current_speed == name else (150, 150, 150)
        pygame.draw.rect(screen, color, rect)
        text = font.render(name, True, (255, 255, 255))
        screen.blit(text, (rect.x + 10, rect.y + 5))

def draw_size_buttons():
    for name, rect in size_buttons.items():
        color = (0, 200, 0) if current_board_size == name else (150, 150, 150)
        pygame.draw.rect(screen, color, rect)
        text = font.render(name, True, (255, 255, 255))
        screen.blit(text, (rect.x + 10, rect.y + 5))

def draw_rule_buttons():
    for name, rect in rule_buttons.items():
        color = (0, 200, 0) if current_rule == name else (150, 150, 150)
        pygame.draw.rect(screen, color, rect)
        text = font.render(name, True, (255, 255, 255))
        screen.blit(text, (rect.x + 10, rect.y + 5))

def draw_file_buttons():
    for name, rect in file_buttons.items():
        color = (0, 200, 0) if current_file == name else (150, 150, 150)
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
                    file = BOARD_FILES[current_file] if current_file else None
                    engine = GameOfLife(width=width, height=height, rules=rules, file=file)
                    board = engine.board
                    rows = len(board)
                    cols = len(board[0])
            elif exit_button.collidepoint(event.pos):
                running = False
            elif settings_button.collidepoint(event.pos):
                current_view = "settings" if current_view == "game" else "game"
            elif reset_button.collidepoint(event.pos) and engine is not None:
                engine = None
                board = None
                rows = 0
                cols = 0
                offset_x = 0
                offset_y = 0
                paused = True
                last_update = time.time()
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
                for name, rect in file_buttons.items():
                    if rect.collidepoint(event.pos) and engine is None:
                        current_file = name
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                offset_x -= Config.SCROLL_SPEED
            elif event.key == pygame.K_RIGHT:
                offset_x += Config.SCROLL_SPEED
            elif event.key == pygame.K_UP:
                offset_y -= Config.SCROLL_SPEED
            elif event.key == pygame.K_DOWN:
                offset_y += Config.SCROLL_SPEED
        elif event.type == pygame.MOUSEWHEEL:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            old_size = cell_size

            if event.y > 0:
                cell_size = min(cell_size * Config.ZOOM_FACTOR, Config.MAX_CELL_SIZE)
            elif event.y < 0:
                cell_size = max(cell_size / Config.ZOOM_FACTOR, Config.MIN_CELL_SIZE)

            scale = cell_size / old_size
            offset_x = (offset_x + mouse_x) * scale - mouse_x
            offset_y = (offset_y + mouse_y) * scale - mouse_y
        mouse_x, mouse_y = pygame.mouse.get_pos()
    screen.fill((0, 0, 0))
    
    if board is not None:
        max_x = max(0, len(board[0]) * cell_size - Config.GAME_WIDTH)
        max_y = max(0, len(board) * cell_size - Config.WINDOW_HEIGHT)

        offset_x = max(0, min(offset_x, max_x))
        offset_y = max(0, min(offset_y, max_y))

    if current_view == "game" and board is not None:
        for i, row in enumerate(board):
            for j, cell in enumerate(row):
                if cell != Config.DEAD:
                    color = Config.CELL_COLORS.get(cell, (255, 0, 0))

                    x = j * cell_size - offset_x
                    y = i * cell_size - offset_y

                    if -Config.CELL_SIZE < x < Config.GAME_WIDTH and -Config.CELL_SIZE < y < Config.WINDOW_HEIGHT:
                        pygame.draw.rect(
                            screen,
                            color,
                            (int(x), int(y), int(cell_size), int(cell_size))
                        )

        if not paused:
            now = time.time()
            if now - last_update >= SPEEDS[current_speed]:
                engine.step()
                board = engine.board
                last_update = now

    elif current_view == "settings":
        screen.fill((20, 20, 20))

        screen.blit(font.render("Speed", True, (255,255,255)), (50, 30))
        screen.blit(font.render("Board Size", True, (255,255,255)), (50, 130))
        screen.blit(font.render("Rules", True, (255,255,255)), (50, 230))
        screen.blit(font.render("Patterns", True, (255,255,255)), (50, 330))
        
        draw_speed_buttons()
        draw_size_buttons()
        draw_rule_buttons()
        draw_file_buttons()

    pygame.draw.rect(
        screen,
        (30, 30, 30),
        (Config.GAME_WIDTH, 0, Config.UI_WIDTH, Config.WINDOW_HEIGHT)
    )

    draw_buttons()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
