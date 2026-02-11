import os
import random
import threading
from typing import Callable
import keyboard
from time import sleep


class GameOfLife():

    def __init__(
        self,
        board_width: int = 80,
        board_height: int = 40,
        rules: Callable[[list[list[int]], int, int], int] | None = None
    ) -> None:
        self.DEAD: int = 0
        self.ALIVE: int = 1
        self.running: bool = True
        self.game: bool = False
        self.board_width = board_width
        self.board_height = board_height
        self.interval_s: float = 0.5
        self.rules = rules if rules else self.classic_rules

    def dead_state(self, width: int, height: int) -> list[list[int]]:
        """Return a grid of DEAD cell of size height x width."""
        return [[0 for _ in range(width)] for _ in range(height)] 

    def random_state(self, width: int, height: int) -> list[list[int]]:
        """Return a grid of size height x width filled with random 0/1 values."""
        return [
            [random.choice([self.DEAD, self.ALIVE]) for _ in range(width)]
            for _ in range(height)
        ]

    def render(self, board_state: list[list[int]]) -> str:
        """Return a visual str of a board state that can be print in the terminal."""
        mapping_dead_alive: dict[int, str] = {0: "⬛", 1: "⬜"}

        return "\n".join(
            "".join(mapping_dead_alive[cell] for cell in row)
            for row in board_state
            )

    def classic_rules(self, previous_board:list[list[int]], i: int, j: int) -> int:
        """Calcul method for the classic rules of the game of life."""
        alive_neighbors = 0

        for transposition_i, transposition_j in [
            (-1, -1), (-1, 0),  (-1, 1),
            (0, -1),            (0, 1),
            (1, -1), (1, 0),  (1, 1)    
        ]:
            new_i = i + transposition_i
            new_j = j + transposition_j

            if 0 <= new_i < self.board_height and 0 <= new_j < self.board_width:
                if previous_board[new_i][new_j] == self.ALIVE:
                    alive_neighbors += 1
        
        if alive_neighbors == 3 or (previous_board[i][j] == self.ALIVE and alive_neighbors == 2):
            return self.ALIVE
        return self.DEAD

    def next_board_state(self, board_state: list[list[int]]) -> list[list[int]]:
        """Return the next board state given a board, following the classic rules of the game of life."""
        result = self.dead_state(self.board_width, self.board_height)

        for i in range(self.board_height):
            for j in range(self.board_width):
                result[i][j] = self.rules(board_state, i, j)

        return result
    
    def pause(self) -> None:
        """Pause the game."""
        self.running = False

    def resume(self) -> None:
        """Resume the game."""
        self.running = True

    def stop(self) -> None:
        """Stop the game."""
        self.game = False

    def listen_keyboard(self) -> None:
        """Listen for space imput on keyboard."""
        while self.game:
            if keyboard.is_pressed("space"):
                if self.running:
                    self.pause()
                else:
                    self.resume()
                sleep(0.1)
            elif keyboard.is_pressed("q"):
                self.stop()
            sleep(0.05)

    def start(self) -> None:
        """Run the game of life in the terminal."""
        self.game = True

        thread = threading.Thread(target=self.listen_keyboard)
        thread.start()

        board = self.random_state(self.board_width, self.board_height)

        while self.game:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(self.render(board))
            if self.running:
                board = self.next_board_state(board)
            sleep(self.interval_s)
        os.system('cls' if os.name == 'nt' else 'clear')


GameOfLife().start()



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
