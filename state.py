import random
from typing import Callable

from constants import ALIVE, DEAD


def dead_state(width: int, height: int) -> list[list[int]]:
    """Return a grid of DEAD cell of size height x width."""
    return [[DEAD for _ in range(width)] for _ in range(height)] 

def random_state(width: int, height: int) -> list[list[int]]:
    """Return a grid of size height x width filled with random 0/1 values."""
    return [
        [random.choice([DEAD, ALIVE]) for _ in range(width)]
        for _ in range(height)
    ]

def next_board_state(board: list[list[int]], rule: Callable[[int, int], int], ever_alive: set) -> tuple[list[list[int]], set[tuple[int, int]]]:
    """Return the next board state given a board, following the classic rules of the game of life."""
    width = len(board[0])
    height = len(board)
    result = dead_state(width, height)

    new_alive_cells = []

    for i in range(height):
        for j in range(width):
            cell_state = rule(board, i, j, ever_alive)
            if cell_state == ALIVE:
                new_alive_cells.append((i,j))
            result[i][j] = cell_state


    ever_alive.update(new_alive_cells)

    return result, ever_alive
