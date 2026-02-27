from config import Config
from game_of_life import next_board_state


def test_next_board_state_dead_cell_rule():
    """Test makes sure that DEAD cells with no live neighbors stay DEAD."""
    board = [
        [Config.DEAD, Config.DEAD, Config.DEAD],
        [Config.DEAD, Config.DEAD, Config.DEAD],
        [Config.DEAD, Config.DEAD, Config.DEAD],
    ]

    result_board = next_board_state(board)

    assert result_board[1][1] == Config.DEAD

def test_next_board_state_dead_cell_live_rule():
    """Test makes sure that DEAD cells with 3 live neighbors come ALIVE."""
    board = [
        [Config.ALIVE, Config.DEAD, Config.DEAD],
        [Config.ALIVE, Config.DEAD, Config.DEAD],
        [Config.ALIVE, Config.DEAD, Config.DEAD],
    ]

    result_board = next_board_state(board)

    assert result_board[1][1] == Config.ALIVE


def test_next_board_state_blinker():
    """Test to makes sure that a Blinker works."""
    blinker_board = [
        [Config.DEAD, Config.ALIVE, Config.DEAD],
        [Config.DEAD, Config.ALIVE, Config.DEAD],
        [Config.DEAD, Config.ALIVE, Config.DEAD],
    ]

    expected = [
        [Config.DEAD, Config.DEAD, Config.DEAD],
        [Config.ALIVE, Config.ALIVE, Config.ALIVE],
        [Config.DEAD, Config.DEAD, Config.DEAD],
    ]

    assert next_board_state(blinker_board) == expected

def test_next_board_state_alive_cell_overpopulation():
    """Check that live cells die when they have more than 3 live neighbors"""
    board = [
        [Config.DEAD, Config.ALIVE, Config.DEAD],
        [Config.ALIVE, Config.ALIVE, Config.ALIVE],
        [Config.DEAD, Config.ALIVE, Config.DEAD],
    ]

    result_board = next_board_state(board)

    assert result_board[1][1] == Config.DEAD

def test_next_board_state_alive_cell_underpopulation():
    """Check that live cells die when they have less than 3 live neighbors"""
    board = [
        [Config.DEAD, Config.DEAD, Config.ALIVE],
        [Config.DEAD, Config.ALIVE, Config.DEAD],
        [Config.DEAD, Config.DEAD, Config.DEAD],
    ]

    result_board = next_board_state(board)

    assert result_board[1][1] == Config.DEAD

def test_next_board_state_corner_cell():
    """Corner cells should not consider out-of-bounds neighbors."""
    board = [
        [Config.DEAD, Config.ALIVE, Config.ALIVE],
        [Config.ALIVE, Config.DEAD, Config.DEAD],
        [Config.DEAD, Config.DEAD, Config.DEAD],
    ]

    result_board = next_board_state(board)

    assert result_board[0][0] == Config.DEAD


def test_next_board_state_border_cell():
    """Edge cells should correctly count neighbors without index errors."""
    board = [
        [Config.DEAD, Config.DEAD, Config.DEAD],
        [Config.ALIVE, Config.ALIVE, Config.ALIVE],
        [Config.DEAD, Config.DEAD, Config.DEAD],
    ]

    result_board = next_board_state(board)

    assert result_board[2][1] == Config.ALIVE
