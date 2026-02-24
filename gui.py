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

start_button = pygame.Rect(MARGIN, rows*CELL_SIZE + MARGIN, BUTTON_WIDTH, BUTTON_HEIGHT)
exit_button = pygame.Rect(MARGIN*2 + BUTTON_WIDTH, rows*CELL_SIZE + MARGIN, BUTTON_WIDTH, BUTTON_HEIGHT)

font = pygame.font.Font(None, 30)

def draw_buttons():
    pygame.draw.rect(screen, (0, 200, 0) if paused else (200, 0, 0), start_button)
    text = font.render("Start" if paused else "Pause", True, (255, 255, 255))
    screen.blit(text, (start_button.x + 10, start_button.y + 5))

    pygame.draw.rect(screen, (0, 0, 200), exit_button)
    text = font.render("Exit", True, (255, 255, 255))
    screen.blit(text, (exit_button.x + 25, exit_button.y + 5))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos):
                paused = not paused
            elif exit_button.collidepoint(event.pos):
                running = False

    screen.fill((0, 0, 0))

    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == 1:
                pygame.draw.rect(
                    screen,
                    (255, 255, 255),
                    (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                )

    draw_buttons()

    if not paused:
        engine.step()
        board = engine.board

    pygame.display.flip()
    clock.tick(5)

pygame.quit()
