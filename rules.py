import random

from constants import ALIVE, DEAD, ZOMBIE


MOORE_NEIGHBORS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1), (1, 0),   (1, 1)
]

VON_NEUMANN_NEIGHBORS = [
    (-1, 0),
    (0, -1), (0, 1),
    (1, 0)
]


def count_neighbors(board, i, j, neighbors, states_to_count):
    height = len(board)
    width = len(board[0])

    counts = {state: 0 for state in states_to_count}

    for di, dj in neighbors:
        ni = i + di
        nj = j + dj

        if 0 <= ni < height and 0 <= nj < width:
            cell = board[ni][nj]
            if cell in counts:
                counts[cell] += 1

    return counts


def classic_logic(cell, alive_neighbors):
    if alive_neighbors == 3 or (cell == ALIVE and alive_neighbors == 2):
        return ALIVE
    return DEAD


def classic_rules(board, i, j, ever_alive):
    """Calcul method of the next state of one cell for the classic rules of the game of life."""
    counts = count_neighbors(
        board, i, j,
        MOORE_NEIGHBORS,
        {ALIVE}
    )

    return classic_logic(board[i][j], counts[ALIVE])


def respawn_rules(board, i, j, ever_alive):
    """Dead cell have a 20% chance of respawing if they were ever alive."""
    counts = count_neighbors(
        board, i, j,
        MOORE_NEIGHBORS,
        {ALIVE}
    )

    current = board[i][j]
    alive_neighbors = counts[ALIVE]

    if (
        current == DEAD
        and (i, j) in ever_alive
        and random.random() <= 0.01
    ):
        return ALIVE

    return classic_logic(current, alive_neighbors)


def zombie_rules(board, i, j, ever_alive):
    counts = count_neighbors(
        board, i, j,
        MOORE_NEIGHBORS,
        {ALIVE, ZOMBIE}
    )

    current = board[i][j]
    alive_neighbors = counts[ALIVE]
    zombie_neighbors = counts[ZOMBIE]

    if current == ALIVE:
        if random.randint(1, 1000) == 1:
            return ZOMBIE
        if alive_neighbors == 0 and zombie_neighbors >= 1:
            return ZOMBIE

    if current == ZOMBIE:
        return ZOMBIE

    return classic_logic(current, alive_neighbors)


def von_neumann_rules(board, i, j, ever_alive):
    counts = count_neighbors(
        board, i, j,
        VON_NEUMANN_NEIGHBORS,
        {ALIVE}
    )

    current = board[i][j]
    alive_neighbors = counts[ALIVE]

    if current == ALIVE:
        return ALIVE if alive_neighbors == 2 else DEAD

    if current == DEAD:
        return ALIVE if alive_neighbors == 3 else DEAD
