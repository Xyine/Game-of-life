import random


DEAD = 0
ALIVE = 1
ZOMBIE = 2


def classic_rules(board: list[list[int]], i: int, j: int, ever_alive: set) -> int:
    """Calcul method of the next state of one cell for the classic rules of the game of life."""
    board_width = len(board[0])
    board_height = len(board)
    alive_neighbors = 0

    for transposition_i, transposition_j in [
        (-1, -1), (-1, 0),  (-1, 1),
        (0, -1),            (0, 1),
        (1, -1), (1, 0),  (1, 1)    
    ]:
        new_i = i + transposition_i
        new_j = j + transposition_j

        if 0 <= new_i < board_height and 0 <= new_j < board_width:
            if board[new_i][new_j] == ALIVE:
                alive_neighbors += 1
    
    if alive_neighbors == 3 or (board[i][j] == ALIVE and alive_neighbors == 2):
        return ALIVE
    return DEAD

def respawn_rules(board: list[list[int]], i: int, j: int, ever_alive: set) -> int:
    """Classic rules but dead cell have a 20% chance of respawing if they were ever alive."""
    board_width = len(board[0])
    board_height = len(board)
    alive_neighbors = 0

    for transposition_i, transposition_j in [
        (-1, -1), (-1, 0),  (-1, 1),
        (0, -1),            (0, 1),
        (1, -1), (1, 0),  (1, 1)    
    ]:
        new_i = i + transposition_i
        new_j = j + transposition_j

        if 0 <= new_i < board_height and 0 <= new_j < board_width:
            if board[new_i][new_j] == ALIVE:
                alive_neighbors += 1
    
    if alive_neighbors == 3 or (
        board[i][j] == ALIVE and alive_neighbors == 2) or (
        board[i][j] == DEAD  and (i, j) in ever_alive and random.random() <= 0.01
    ) :
        return ALIVE
    
    return DEAD

def zombie_rules(board: list[list[int]], i: int, j: int, ever_alive: set) -> int:
    board_width = len(board[0])
    board_height = len(board)
    alive_neighbors = 0
    zombie_neighbors = 0

    for di, dj in [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]:
        ni = i + di
        nj = j + dj

        if 0 <= ni < board_width and 0 <= nj < board_height:
            if board[ni][nj] == ALIVE:
                alive_neighbors += 1
            elif board[ni][nj] == ZOMBIE:
                zombie_neighbors += 1

    current = board[i][j]

    if current == ALIVE:
        if random.randint(1, 1000) == 1:
            return ZOMBIE
        if alive_neighbors == 0 and zombie_neighbors >= 1:
            return ZOMBIE

    if current == ALIVE:
        if alive_neighbors == 2 or alive_neighbors == 3:
            return ALIVE
        return DEAD

    if current == DEAD:
        if alive_neighbors == 3:
            return ALIVE
        return DEAD

    if current == ZOMBIE:
        return ZOMBIE
    
def von_neumann_rules(board: list[list[int]], i: int, j: int, ever_alive: set) -> int:
    board_width = len(board[0])
    board_height = len(board)
    alive_neighbors = 0

    for di, dj in [
        (-1, 0),
        (0, -1), (0, 1),
        (1, 0)
    ]:
        ni = i + di
        nj = j + dj

        if 0 <= ni < board_height and 0 <= nj < board_width:
            if board[ni][nj] == ALIVE:
                alive_neighbors += 1

    current = board[i][j]

    if current == ALIVE:
        if alive_neighbors == 2:
            return ALIVE
        return DEAD

    if current == DEAD:
        if alive_neighbors == 3:
            return ALIVE
        return DEAD
