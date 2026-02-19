DEAD = 0
ALIVE = 1
ZOMBIE = 2


def detect_block(board, i, j, detected_patterns, used_cells):

    block_cells = [
        (i, j),
        (i, j+1),
        (i+1, j),
        (i+1, j+1)
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

    detected_patterns.append(("block", block_cells))

    for cell in block_cells:
        used_cells.add(cell)

def detect_patterns(board):
    board_width = len(board[0])
    board_height = len(board)
    detected_patterns = []
    used_cells = set()

    for i in range(board_height - 1):
        for j in range(board_width - 1):

            if 0 <= i < board_height and 0 <= j < board_width and board[i][j] == ALIVE:
                detect_block(board, i, j, detected_patterns, used_cells)

    return detected_patterns

def apply_block_colors(rendered_str: str, detected_patterns: list) -> str:
    """ Return str with colored pattern."""
    grid = [list(row) for row in rendered_str.split("\n")]

    for name, cells in detected_patterns:

        if name == "block":
            for (i, j) in cells:
                grid[i][j] = "🟫"

    return "\n".join("".join(row) for row in grid)
