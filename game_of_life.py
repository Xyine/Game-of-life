import json
import os
import random
import threading
from typing import Callable, Literal, Optional
import keyboard
from time import sleep

from pydantic import BaseModel, model_validator

from constants import ALIVE, DEAD, ZOMBIE
from patterns import apply_block_colors, detect_patterns
from rules import classic_rules, zombie_rules, von_neumann_rules, respawn_rules
from state import dead_state, next_board_state, random_state


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
        width: int | None = None,
        height: int | None = None,
        file: str | None = None ,
        interval_s: float = 0.5,
        fill_mode: str = "dead",
        placement: str = "topleft",
        rules: Callable[[int, int], int] | None = None,
        colored_patern: bool = False
    ) -> None:
        self.running: bool = True
        self.game: bool = False
        self.board = self.create_board(file, fill_mode, placement, width, height)
        self.width = len(self.board[0])
        self.height = len(self.board)
        self.interval_s = interval_s
        self.rules = rules if rules else classic_rules
        self.colored_patern = colored_patern
        self.ever_alive = self.create_history()

    def create_history(self) -> set:
        """Create the history of the alive cells."""
        ever_alive = set()
    
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == ALIVE:
                    ever_alive.add((i, j))

        return ever_alive

    def create_board(self, file: str | None, fill_mode: str, placement: str, width: int | None, height: int | None) -> list[list[int]]:
        """Create the board."""
        if file:
            board = self.load_state_from_file(file)

            if height and width:
                board = self.integrate_pattern(
                    board,
                    width,
                    height,
                    fill_mode,
                    placement,
                )
        else:
            width = width if width else 50
            height = height if height else 40
            board = random_state(width, height)

        return board

    def integrate_pattern(
        self,
        pattern: list[list[int]],
        width: int,
        height: int,
        fill_mode: str,
        placement: str
    ) -> list[list[int]]:

        pattern_height = len(pattern)
        pattern_width = len(pattern[0])

        # Refuse if pattern bigger than board
        if pattern_width > width or pattern_height > height:
            raise ValueError(
                "Board is smaller than pattern. "
                f"Pattern size: {pattern_width}x{pattern_height}, "
                f"Board size: {width}x{height}"
            )

        # Create base board
        if fill_mode == "dead":
            board = [[DEAD for _ in range(width)]
                    for _ in range(height)]
        elif fill_mode == "random":
            board = [[random.choice([DEAD, ALIVE])
                    for _ in range(width)]
                    for _ in range(height)]
        else:
            raise ValueError("fill_mode must be 'dead' or 'random'")

        # Place pattern in top-left corner
        if placement == "topleft":
            offset_y = 0
            offset_x = 0
        elif placement == "center":
            offset_y = (height - pattern_height) // 2
            offset_x = (width - pattern_width) // 2
        else:
            raise ValueError("placement must be 'topleft' or 'center'")

        # Place pattern
        for i in range(pattern_height):
            for j in range(pattern_width):
                board[i + offset_y][j + offset_x] = pattern[i][j]

        return board

    def render(self, board_state: list[list[int]]) -> str:
        """Return a visual str of a board state that can be print in the terminal."""
        mapping_dead_alive: dict[int, str] = {DEAD: "⬛", ALIVE: "⬜", ZOMBIE: "🟩"}

        return "\n".join(
            "".join(mapping_dead_alive[cell] for cell in row)
            for row in board_state
            )

    def build_from_coordinates(self, data: BoardFile) -> list[list[int]]:
        """Build a full grid from a coordinate-based board definition."""

        width = data.width
        height = data.height
        alive_cells = data.alive_cells

        board = dead_state(width, height)

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
            if self.colored_patern:
                print(apply_block_colors(self.render(self.board), detect_patterns(self.board)))
            else:
                print(self.render(self.board))
            if self.running:
                self.board, self.ever_alive = next_board_state(self.board, self.rules, self.ever_alive)
            sleep(self.interval_s)
        os.system('cls' if os.name == 'nt' else 'clear')


GameOfLife(colored_patern=True).start()



#========================== OPTIMISATION CORNER ===========================================

def next_board_state_optimized(board_state: list[list[int]]) -> list[list[int]]:
    """Calculate next board state with a padding optimisation."""
    height = len(board_state)
    width = len(board_state[0])

    padded = [[DEAD] * (width + 2)]
    for row in board_state:
        padded.append([DEAD] + row + [DEAD])
    padded.append([DEAD] * (width + 2))

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
                if padded[i + di][j + dj] == ALIVE:
                    compt += 1

            if compt == 3 or (padded[i][j] == ALIVE and compt == 2):
                result[i - 1][j - 1] = ALIVE

    return result
