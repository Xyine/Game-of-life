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

    for i in range(height):
        for j in range(width):
            result[i][j] = rule(board, i, j, ever_alive)

    for i in range(height):
        for j in range(width):
            if result[i][j] == ALIVE:
                ever_alive.add((i, j))

    return result, ever_alive
