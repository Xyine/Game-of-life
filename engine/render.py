from config.config import Config
from engine.patterns import Pattern


def render(board_state: list[list[int]]) -> str:
    """Return a visual str of a board state that can be print in the terminal."""
    mapping_dead_alive: dict[int, str] = {Config.DEAD: "⬛", Config.ALIVE: "⬜", Config.ZOMBIE: "🟩"}

    return "\n".join(
        "".join(mapping_dead_alive[cell] for cell in row)
        for row in board_state
        )

def apply_pattern_colors(rendered_board: str, detected_patterns: list[Pattern]) -> str:
    """ Return str with colored pattern."""
    grid = [list(row) for row in rendered_board.split("\n")]

    for pattern in detected_patterns:

        if pattern.name == "block":
            for (i, j) in pattern.cells:
                grid[i][j] = "🟫"

        if pattern.name == "blinker":
            for (i, j) in pattern.cells:
                grid[i][j] = "🟦"

    return "\n".join("".join(row) for row in grid)
