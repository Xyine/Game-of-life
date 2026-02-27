import os
import threading
from typing import Callable
import keyboard
from time import sleep

from board import create_board, create_history
from config import Config
from patterns import detect_patterns
from render import apply_pattern_colors, render
from rules import classic_rules, zombie_rules, von_neumann_rules, respawn_rules
from state import dead_state, next_board_state


class GameOfLife():

    def __init__(
        self,
        width: int | None = None,
        height: int | None = None,
        file: str | None = None,
        interval_s: float = 0.5,
        fill_mode: str = "DEAD",
        placement: str = "topleft",
        rules: Callable[[int, int], int] | None = None,
        paterns: bool = False
    ) -> None:
        self.running: bool = True
        self.game: bool = False
        self.board = create_board(file, fill_mode, placement, width, height)
        self.width = len(self.board[0])
        self.height = len(self.board)
        self.interval_s = interval_s
        self.rules = rules if rules else classic_rules
        self.paterns = paterns
        self.ever_alive = create_history(self.board)

    def step(self):
        self.board, self.ever_alive = next_board_state(
            self.board,
            self.rules,
            self.ever_alive
        )

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

        thread = threading.Thread(target=self.listen_keyboard, daemon=True) # Automatically terminate the thread when the main program exits
        thread.start()

        while self.game:
            os.system('cls' if os.name == 'nt' else 'clear')
            if self.paterns:
                print(apply_pattern_colors(render(self.board), detect_patterns(self.board)))
            else:
                print(render(self.board))
            if self.running:
                self.board, self.ever_alive = next_board_state(self.board, self.rules, self.ever_alive)
            sleep(self.interval_s)
        os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == "__main__":
    GameOfLife().start()


#========================== OPTIMISATION CORNER ===========================================

def next_board_state_optimized(board_state: list[list[int]]) -> list[list[int]]:
    """Calculate next board state with a padding optimisation."""
    height = len(board_state)
    width = len(board_state[0])

    padded = [[Config.DEAD] * (width + 2)]
    for row in board_state:
        padded.append([Config.DEAD] + row + [Config.DEAD])
    padded.append([Config.DEAD] * (width + 2))

    result = dead_state(width, height)

    transposition_list = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]

    for i in range(1, height + 1):
        for j in range(1, width + 1):
            compt = 0
            for di, dj in transposition_list:
                if padded[i + di][j + dj] == Config.ALIVE:
                    compt += 1

            if compt == 3 or (padded[i][j] == Config.ALIVE and compt == 2):
                result[i - 1][j - 1] = Config.ALIVE

    return result
