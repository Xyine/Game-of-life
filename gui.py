import pygame
from game_of_life import GameOfLife

CELL_SIZE = 15


engine = GameOfLife()

board = engine.board

rows = len(board)
cols = len(board[0])

pygame.init()

screen = pygame.display.set_mode(
    (cols * CELL_SIZE, rows * CELL_SIZE)
)

pygame.display.set_caption("Game of Life")
clock = pygame.time.Clock()

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == 1:
                pygame.draw.rect(
                    screen,
                    (255, 255, 255),
                    (
                        j * CELL_SIZE,
                        i * CELL_SIZE,
                        CELL_SIZE,
                        CELL_SIZE
                    )
                )

    engine.step()

    board = engine.board

    pygame.display.flip()

    clock.tick(5)

pygame.quit()
