from typing import Optional

from constants import ALIVE, DEAD


def detect_block(board: list[list[int]], i: int, j: int, used_cells: set) -> Optional[tuple[str, list[tuple[int, int]]]]:

    block_cells = [
        (i, j),(i, j+1),
        (i+1, j),(i+1, j+1)
    ]

    for (x, y) in block_cells:
        if not (0 <= x < len(board) and 0 <= y < len(board[0])):
            return
        if board[x][y] != ALIVE:
            return
        if (x, y) in used_cells:
            return

    for x in range(i-1, i+3):
        for y in range(j-1, j+3):

            if not (0 <= x < len(board) and 0 <= y < len(board[0])):
                continue

            if (x, y) not in block_cells:
                if board[x][y] != DEAD:
                    return

    for cell in block_cells:
        used_cells.add(cell)
    
    return ("block", block_cells)

def _detect_horizontal_blinker(board: list[list[int]], i: int, j: int, used_cells: set) -> Optional[tuple[str, list[tuple[int, int]]]]:
    horrizontal_blinker_cells = [
        (i, j),(i, j+1),(i, j+2)
    ]

    for (x, y) in horrizontal_blinker_cells:
            if not (0 <= x < len(board) and 0 <= y < len(board[0])):
                return
            if board[x][y] != ALIVE:
                return
            if (x, y) in used_cells:
                return

    for x in range(i-1, i+2):
        for y in range(j-1, j+4):

            if not (0 <= x < len(board) and 0 <= y < len(board[0])):
                continue

            if (x, y) not in horrizontal_blinker_cells:
                if board[x][y] != DEAD:
                    return

    for cell in horrizontal_blinker_cells:
        used_cells.add(cell)
    
    return ("blinker", horrizontal_blinker_cells)

def _detect_vertical_blinker(board: list[list[int]], i: int, j: int, used_cells: set) -> Optional[tuple[str, list[tuple[int, int]]]]:
    vertical_blinker_cell = [
        (i, j),
        (i+1, j),
        (i+2, j)
    ]

    for (x, y) in vertical_blinker_cell:
            if not (0 <= x < len(board) and 0 <= y < len(board[0])):
                return
            if board[x][y] != ALIVE:
                return
            if (x, y) in used_cells:
                return

    for x in range(i-1, i+4):
        for y in range(j-1, j+2):

            if not (0 <= x < len(board) and 0 <= y < len(board[0])):
                continue

            if (x, y) not in vertical_blinker_cell:
                if board[x][y] != DEAD:
                    return

    for cell in vertical_blinker_cell:
        used_cells.add(cell)
    
    return ("blinker", vertical_blinker_cell)

def detect_blinker(board: list[list[int]], i: int, j: int, used_cells: set) -> Optional[tuple[str, list[tuple[int, int]]]]:
    horizontal = _detect_horizontal_blinker(board, i, j, used_cells)
    vertical = _detect_vertical_blinker(board, i, j, used_cells)

    return horizontal or vertical

def detect_patterns(board):
    """Detect block and blinker patterns."""
    width = len(board[0])
    height = len(board)
    detected_patterns = []
    used_cells = set()

    detectors = [detect_block, detect_blinker]

    for i in range(height):
        for j in range(width):
            if board[i][j] != ALIVE:
                continue

            for detect in detectors:
                pattern = detect(board, i, j, used_cells)
                if pattern:
                    detected_patterns.append(pattern)

    return detected_patterns

def apply_pattern_colors(rendered_board: str, detected_patterns: list) -> str:
    """ Return str with colored pattern."""
    grid = [list(row) for row in rendered_board.split("\n")]

    for name, cells in detected_patterns:

        if name == "block":
            for (i, j) in cells:
                grid[i][j] = "🟫"

        if name == "blinker":
            for (i, j) in cells:
                grid[i][j] = "🟦"

    return "\n".join("".join(row) for row in grid)
