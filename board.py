import json
import random
from typing import Literal, Optional

from pydantic import BaseModel, model_validator
from constants import ALIVE, DEAD
from state import dead_state, random_state


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


def create_history(board, width, height) -> set:
    """Create the history of the alive cells."""
    ever_alive = set()

    for i in range(height):
        for j in range(width):
            if board[i][j] == ALIVE:
                ever_alive.add((i, j))

    return ever_alive

def create_board(file: str | None, fill_mode: str, placement: str, width: int | None, height: int | None) -> list[list[int]]:
    """Create the board."""
    if file:
        board = load_state_from_file(file)

        if height and width:
            board = integrate_pattern(
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

def build_from_coordinates(data: BoardFile) -> list[list[int]]:
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

        board[row][col] = ALIVE

    return board

def load_state_from_file(path: str) -> list[list[int]]:
    """Return a valid board from a file."""
    with open(path) as f:
        json_data = json.load(f)
    
    data = BoardFile.model_validate(json_data)

    if data.format == "grid":
        return data.grid
    else:
        return build_from_coordinates(data)
