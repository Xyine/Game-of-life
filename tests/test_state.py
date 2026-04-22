import pytest

from config.config import Config
from engine.state import dead_state, next_board_state
from rules.rules import classic_rules


D = Config.DEAD
A = Config.ALIVE


def alive_cells(board):
    return {
        (i, j)
        for i, row in enumerate(board)
        for j, cell in enumerate(row)
        if cell == A
    }


def step(board, ever_alive=None):
    if ever_alive is None:
        ever_alive = alive_cells(board)
    return next_board_state(board, classic_rules, ever_alive)


def test_dead_state_returns_grid_with_expected_dimensions():
    board = dead_state(4, 3)

    assert len(board) == 3
    assert all(len(row) == 4 for row in board)
    assert all(cell == D for row in board for cell in row)


def test_dead_cell_with_three_neighbors_becomes_alive():
    board = [
        [A, D, D],
        [A, D, D],
        [A, D, D],
    ]

    next_board, ever_alive = step(board)

    assert next_board[1][1] == A
    assert (1, 1) in ever_alive


def test_dead_cell_with_fewer_than_three_neighbors_stays_dead():
    board = [
        [D, D, D],
        [D, D, D],
        [D, A, D],
    ]

    next_board, _ = step(board)

    assert next_board[1][1] == D


@pytest.mark.parametrize(
    "board",
    [
        [
            [D, A, D],
            [D, A, A],
            [D, D, D],
        ],
        [
            [D, D, D],
            [A, A, D],
            [D, A, D],
        ],
    ],
)
def test_alive_cell_with_two_or_three_neighbors_survives(board):
    next_board, _ = step(board)

    assert next_board[1][1] == A


def test_alive_cell_with_fewer_than_two_neighbors_dies():
    board = [
        [D, D, A],
        [D, A, D],
        [D, D, D],
    ]

    next_board, _ = step(board)

    assert next_board[1][1] == D


def test_alive_cell_with_more_than_three_neighbors_dies():
    board = [
        [D, A, D],
        [A, A, A],
        [D, A, D],
    ]

    next_board, _ = step(board)

    assert next_board[1][1] == D


def test_block_still_life_remains_unchanged():
    board = [
        [D, D, D, D],
        [D, A, A, D],
        [D, A, A, D],
        [D, D, D, D],
    ]

    next_board, _ = step(board)

    assert next_board == board


def test_blinker_oscillates_from_vertical_to_horizontal():
    board = [
        [D, A, D],
        [D, A, D],
        [D, A, D],
    ]

    expected = [
        [D, D, D],
        [A, A, A],
        [D, D, D],
    ]

    next_board, _ = step(board)

    assert next_board == expected


def test_blinker_returns_to_initial_state_after_two_steps():
    board = [
        [D, A, D],
        [D, A, D],
        [D, A, D],
    ]

    next_board, ever_alive = step(board)
    second_board, _ = step(next_board, ever_alive)

    assert second_board == board


def test_next_board_state_preserves_board_dimensions():
    board = [
        [D, A, D, D],
        [A, A, D, D],
        [D, D, D, A],
    ]

    next_board, _ = step(board)

    assert len(next_board) == len(board)
    assert all(len(next_row) == len(row) for next_row, row in zip(next_board, board))


def test_ever_alive_accumulates_cells_seen_alive_over_time():
    board = [
        [A, D, D],
        [A, D, D],
        [A, D, D],
    ]

    initial_history = {(0, 0), (1, 0), (2, 0)}

    _, ever_alive = step(board, initial_history)

    assert ever_alive == {(0, 0), (1, 0), (2, 0), (1, 1)}
