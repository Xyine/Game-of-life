import random

from config import Config


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
    if alive_neighbors == 3 or (cell == Config.ALIVE and alive_neighbors == 2):
        return Config.ALIVE
    return Config.DEAD


def classic_rules(board, i, j, ever_alive):
    """Calcul method of the next state of one cell for the classic rules of the game of life."""
    counts = count_neighbors(
        board, i, j,
        MOORE_NEIGHBORS,
        {Config.ALIVE}
    )

    return classic_logic(board[i][j], counts[Config.ALIVE])


def respawn_rules(board, i, j, ever_alive):
    """DEAD cell have a 20% chance of respawing if they were ever ALIVE."""
    counts = count_neighbors(
        board, i, j,
        MOORE_NEIGHBORS,
        {Config.ALIVE}
    )

    current = board[i][j]
    alive_neighbors = counts[Config.ALIVE]

    if (
        current == Config.DEAD
        and (i, j) in ever_alive
        and random.random() <= 0.01
    ):
        return Config.ALIVE

    return classic_logic(current, alive_neighbors)


def zombie_rules(board, i, j, ever_alive):
    counts = count_neighbors(
        board, i, j,
        MOORE_NEIGHBORS,
        {Config.ALIVE, Config.ZOMBIE}
    )

    current = board[i][j]
    alive_neighbors = counts[Config.ALIVE]
    zombie_neighbors = counts[Config.ZOMBIE]

    if current == Config.ALIVE:
        if random.randint(1, 1000) == 1:
            return Config.ZOMBIE
        if alive_neighbors == 0 and zombie_neighbors >= 1:
            return Config.ZOMBIE

    if current == Config.ZOMBIE:
        return Config.ZOMBIE

    return classic_logic(current, alive_neighbors)


def von_neumann_rules(board, i, j, ever_alive):
    counts = count_neighbors(
        board, i, j,
        VON_NEUMANN_NEIGHBORS,
        {Config.ALIVE}
    )

    current = board[i][j]
    alive_neighbors = counts[Config.ALIVE]

    if current == Config.ALIVE:
        return Config.ALIVE if alive_neighbors == 2 else Config.DEAD

    if current == Config.DEAD:
        return Config.ALIVE if alive_neighbors == 3 else Config.DEAD
