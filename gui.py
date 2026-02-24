import pygame
from game_of_life import GameOfLife


CELL_SIZE = 15
BUTTON_HEIGHT = 40
BUTTON_WIDTH = 100
MARGIN = 10


engine = GameOfLife()
board = engine.board
rows = len(board)
cols = len(board[0])


pygame.init()
screen = pygame.display.set_mode(
    (cols * CELL_SIZE, rows * CELL_SIZE + BUTTON_HEIGHT + MARGIN*2)
)
pygame.display.set_caption("Game of Life")
clock = pygame.time.Clock()


running = True
paused = True
current_view = "game"
tick_rate = 5


start_button = pygame.Rect(MARGIN, rows*CELL_SIZE + MARGIN, BUTTON_WIDTH, BUTTON_HEIGHT)
exit_button = pygame.Rect(MARGIN*2 + BUTTON_WIDTH, rows*CELL_SIZE + MARGIN, BUTTON_WIDTH, BUTTON_HEIGHT)
settings_button = pygame.Rect(MARGIN*3 + BUTTON_WIDTH*2, rows*CELL_SIZE + MARGIN, BUTTON_WIDTH, BUTTON_HEIGHT)


input_rect = pygame.Rect(50, 50, 100, 40)
active_input = False
input_text = str(tick_rate)


font = pygame.font.Font(None, 30)


def draw_buttons():
    # Start/Pause button
    pygame.draw.rect(screen, (0, 200, 0) if paused else (200, 0, 0), start_button)
    text = font.render("Start" if paused else "Pause", True, (255, 255, 255))
    screen.blit(text, (start_button.x + 10, start_button.y + 5))

    # Exit button
    pygame.draw.rect(screen, (0, 0, 200), exit_button)
    text = font.render("Exit", True, (255, 255, 255))
    screen.blit(text, (exit_button.x + 25, exit_button.y + 5))

    # Settings button
    pygame.draw.rect(screen, (150, 150, 0), settings_button)
    text = font.render("Settings", True, (255, 255, 255))
    screen.blit(text, (settings_button.x + 5, settings_button.y + 5))


def draw_input():
    label = font.render("Speed (1 - 120):", True, (255, 255, 255))
    screen.blit(label, (input_rect.x, input_rect.y - 25))

    pygame.draw.rect(screen, (255, 255, 255) if active_input else (150, 150, 150), input_rect, 2)
    
    txt_surface = font.render(input_text, True, (255, 255, 255))
    screen.blit(txt_surface, (input_rect.x + 5, input_rect.y + 5))


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos):
                paused = not paused
            elif exit_button.collidepoint(event.pos):
                running = False
            elif settings_button.collidepoint(event.pos):
                current_view = "settings" if current_view == "game" else "game"
            elif input_rect.collidepoint(event.pos) and current_view == "settings":
                active_input = True
            else:
                active_input = False
        elif event.type == pygame.KEYDOWN and active_input:
            if event.key == pygame.K_RETURN:
                try:
                    tick_rate = min(max(1, int(input_text)), 120)
                except ValueError:
                    tick_rate = 5
                active_input = False
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                if event.unicode.isdigit():
                    input_text += event.unicode

    screen.fill((0, 0, 0))

    if current_view == "game":
        for i, row in enumerate(board):
            for j, cell in enumerate(row):
                if cell == 1:
                    pygame.draw.rect(
                        screen,
                        (255, 255, 255),
                        (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    )
        if not paused:
            engine.step()
            board = engine.board

    elif current_view == "settings":
        screen.fill((20, 20, 20))
        draw_input()

    draw_buttons()

    pygame.display.flip()
    clock.tick(tick_rate)

pygame.quit()
