import json
import os
import random
import threading
from typing import Callable, Literal, Optional
import keyboard
from time import sleep

from pydantic import BaseModel, model_validator


class BoardFile(BaseModel):
    format: Literal["grid", "coordinates"]

    # grid format
    grid: Optional[list[list[int]]] = None

    # coordinate format
    width: Optional[int] = None
    height: Optional[int] = None
    alive_cells: Optional[list[list[int]]] = None

    @model_validator(mode="after")
    def validate_structure(self):
        if self.format == "grid":
            if self.grid is None:
                raise ValueError("Grid format requires 'grid'")
        elif self.format == "coordinates":
            if None in (self.width, self.height, self.alive_cells):
                raise ValueError("Coordinates format requires width, height and alive_cells")
        return self
    

class GameOfLife():

    def __init__(
        self,
        board_width: int | None = None,
        board_height: int | None = None,
        board_file: str | None = None ,
        interval_s: float = 0.5,
        fill_mode: str = "dead",
        rules: Callable[[int, int], int] | None = None
    ) -> None:
        self.DEAD: int = 0
        self.ALIVE: int = 1
        self.running: bool = True
        self.game: bool = False
        if board_file:
            self.board = self.load_state_from_file(board_file)
            self.board_width = board_width if board_width else len(self.board[0])
            self.board_height = board_height if board_height else len(self.board)
            
            if board_height and board_width:
                self.board = self.integrate_pattern(
                    self.board,
                    self.board_width,
                    self.board_height,
                    fill_mode
                )
        else:
            if board_width is None or board_height is None:
                self.board_width, self.board_height = 50, 40

            self.board = self.random_state(board_width, board_height)
        self.interval_s: float = interval_s
        self.rules = rules if rules else self.classic_rules

    def dead_state(self, width: int, height: int) -> list[list[int]]:
        """Return a grid of DEAD cell of size height x width."""
        return [[self.DEAD for _ in range(width)] for _ in range(height)] 

    def random_state(self, width: int, height: int) -> list[list[int]]:
        """Return a grid of size height x width filled with random 0/1 values."""
        return [
            [random.choice([self.DEAD, self.ALIVE]) for _ in range(width)]
            for _ in range(height)
        ]

    def integrate_pattern(
        self,
        pattern: list[list[int]],
        board_width: int,
        board_height: int,
        fill_mode: str = "dead"
    ) -> list[list[int]]:

        pattern_height = len(pattern)
        pattern_width = len(pattern[0])

        # Refuse if pattern bigger than board
        if pattern_width > board_width or pattern_height > board_height:
            raise ValueError(
                "Board is smaller than pattern. "
                f"Pattern size: {pattern_width}x{pattern_height}, "
                f"Board size: {board_width}x{board_height}"
            )

        # Create base board
        if fill_mode == "dead":
            board = [[self.DEAD for _ in range(board_width)]
                    for _ in range(board_height)]
        elif fill_mode == "random":
            board = [[random.choice([self.DEAD, self.ALIVE])
                    for _ in range(board_width)]
                    for _ in range(board_height)]
        else:
            raise ValueError("fill_mode must be 'dead' or 'random'")

        # Place pattern in top-left corner
        for i in range(pattern_height):
            for j in range(pattern_width):
                board[i][j] = pattern[i][j]

        return board

    def render(self, board_state: list[list[int]]) -> str:
        """Return a visual str of a board state that can be print in the terminal."""
        mapping_dead_alive: dict[int, str] = {0: "⬛", 1: "⬜"}

        return "\n".join(
            "".join(mapping_dead_alive[cell] for cell in row)
            for row in board_state
            )

    def classic_rules(self, i: int, j: int) -> int:
        """Calcul method of the next state of one cell for the classic rules of the game of life."""
        alive_neighbors = 0

        for transposition_i, transposition_j in [
            (-1, -1), (-1, 0),  (-1, 1),
            (0, -1),            (0, 1),
            (1, -1), (1, 0),  (1, 1)    
        ]:
            new_i = i + transposition_i
            new_j = j + transposition_j

            if 0 <= new_i < self.board_height and 0 <= new_j < self.board_width:
                if self.board[new_i][new_j] == self.ALIVE:
                    alive_neighbors += 1
        
        if alive_neighbors == 3 or (self.board[i][j] == self.ALIVE and alive_neighbors == 2):
            return self.ALIVE
        return self.DEAD

    def next_board_state(self) -> list[list[int]]:
        """Return the next board state given a board, following the classic rules of the game of life."""
        result = self.dead_state(self.board_width, self.board_height)

        for i in range(self.board_height):
            for j in range(self.board_width):
                result[i][j] = self.rules(i, j)

        return result
    
    def build_from_coordinates(self, data: BoardFile) -> list[list[int]]:
        """Build a full grid from a coordinate-based board definition."""

        width = data.width
        height = data.height
        alive_cells = data.alive_cells

        board = [[0 for _ in range(width)] for _ in range(height)]

        for cell in alive_cells:
            if len(cell) != 2:
                raise ValueError("Each alive cell must contain exactly two integers")

            row, col = cell

            if not (0 <= row < height and 0 <= col < width):
                raise ValueError(
                    f"Alive cell ({row}, {col}) is outside board bounds "
                    f"(height={height}, width={width})"
                )

            board[row][col] = 1

        return board

    def load_state_from_file(self, path: str) -> list[list[int]]:
        """Return a valid board from a file."""
        with open(path) as f:
            json_data = json.load(f)
        
        data = BoardFile.model_validate(json_data)

        if data.format == "grid":
            return data.grid
        else:
            return self.build_from_coordinates(data)


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
            print(self.render(self.board))
            if self.running:
                self.board = self.next_board_state()
            sleep(self.interval_s)
        os.system('cls' if os.name == 'nt' else 'clear')


GameOfLife(board_file="blinker.json").start()



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
