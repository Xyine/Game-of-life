import os
import random
import threading
import keyboard
from time import sleep


DEAD = 0
ALIVE = 1
running = True

def dead_state(width: int, height: int) -> list[list[int]]:
    return [[0 for _ in range(width)] for _ in range(height)] 


def random_state(width: int, height: int) -> list[list[int]]:
    """Return a grid of size height x width filled with random 0/1 values."""
    return [[random.choice([DEAD, ALIVE]) for _ in range(width)] for _ in range(height)]


def render(board_state: list[list[int]]) -> str:
    """Return a visual str of a board state that can be print in the terminal."""
    mapping_dead_alive: dict[int, str] = {0: "⬛", 1: "⬜"}

    return "\n".join(
        "".join(mapping_dead_alive[cell] for cell in row)
        for row in board_state
        )


def next_board_state(board_state: list[list[int]]) -> list[list[int]]:
    """Return the next board state given a board, following the classic rules of the game of life."""
    board_width = len(board_state[0])
    board_height = len(board_state)

    result = dead_state(board_width, board_height)

    transposition_list = [
        (-1, -1), (-1, 0), (-1, +1),
        (0, -1), (0, +1),
        (+1, -1), (+1, 0), (+1, +1)    
    ]

    for i in range(board_height):
        for j in range(board_width):
            compt = 0
            
            for transposition_i, transposition_j in transposition_list:
                new_i = i + transposition_i
                new_j = j + transposition_j

                if 0 <= new_i < board_height and 0 <= new_j < board_width:
                    if board_state[new_i][new_j] == ALIVE:
                        compt += 1
            
            if compt == 3 or (board_state[i][j] == ALIVE and compt == 2):
                result[i][j] = ALIVE
            else:
                result[i][j] = DEAD

    return result


def listen_keyboard():
    """Listen for space imput on keyboard."""
    while True:
        if keyboard.is_pressed("space"):
            global running
            running = not running
        sleep(0.1)


def run_life(board_width: int = 80, board_height: int = 40, interval_s: float = 0.5) -> None:
    """Run the game of life in the terminal."""
    
    thread = threading.Thread(target=listen_keyboard)
    thread.start()

    board = random_state(board_width, board_height)

    while True:
        os.system('clear')
        print(render(board))
        if running:
            board = next_board_state(board)
        sleep(interval_s)


run_life()



#========================== OPTIMISATION CORNER ===========================================

def next_board_state_optimized(board_state: list[list[int]]) -> list[list[int]]:
    """Calculate next board state with a padding optimisation."""
    board_height = len(board_state)
    board_width = len(board_state[0])

    padded = [[DEAD] * (board_width + 2)]
    for row in board_state:
        padded.append([DEAD] + row + [DEAD])
    padded.append([DEAD] * (board_width + 2))

    result = dead_state(board_width, board_height)

    transposition_list = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]

    for i in range(1, board_height + 1):
        for j in range(1, board_width + 1):
            compt = 0
            for di, dj in transposition_list:
                if padded[i + di][j + dj] == ALIVE:
                    compt += 1

            if compt == 3 or (padded[i][j] == ALIVE and compt == 2):
                result[i - 1][j - 1] = ALIVE

    return result
