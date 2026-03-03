from config.config import Config
from engine.game_of_life import next_board_state
from rules.rules import classic_rules

def test_next_board_state_dead_cell_rule():
    """Test makes sure that DEAD cells with no live neighbors stay DEAD."""
    board = [
        [Config.DEAD, Config.DEAD, Config.DEAD],
        [Config.DEAD, Config.DEAD, Config.DEAD],
        [Config.DEAD, Config.DEAD, Config.DEAD],
    ]

    result_board, ever_alive = next_board_state(board, classic_rules, set())

    assert result_board[1][1] == Config.DEAD
    assert not ever_alive

def test_next_board_state_dead_cell_live_rule():
    """Test makes sure that DEAD cells with 3 live neighbors come ALIVE."""
    board = [
        [Config.ALIVE, Config.DEAD, Config.DEAD],
        [Config.ALIVE, Config.DEAD, Config.DEAD],
        [Config.ALIVE, Config.DEAD, Config.DEAD],
    ]

    result_board, ever_alive = next_board_state(board, classic_rules, {(0,0), (1,0), (2,0)})

    assert result_board[1][1] == Config.ALIVE
    assert (1,1) in ever_alive

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

    return_board, ever_alive = next_board_state(blinker_board, classic_rules, {(0,1), (1,1), (2,1)})

    assert return_board == expected
    assert (2, 2) not in ever_alive

def test_next_board_state_alive_cell_overpopulation():
    """Check that live cells die when they have more than 3 live neighbors"""
    board = [
        [Config.DEAD, Config.ALIVE, Config.DEAD],
        [Config.ALIVE, Config.ALIVE, Config.ALIVE],
        [Config.DEAD, Config.ALIVE, Config.DEAD],
    ]

    result_board, ever_alive = next_board_state(board, classic_rules, {(0,1), (1,0), (1,1), (1,2), (2,1)})

    assert result_board[1][1] == Config.DEAD

def test_next_board_state_alive_cell_underpopulation():
    """Check that live cells die when they have less than 3 live neighbors"""
    board = [
        [Config.DEAD, Config.DEAD, Config.ALIVE],
        [Config.DEAD, Config.ALIVE, Config.DEAD],
        [Config.DEAD, Config.DEAD, Config.DEAD],
    ]

    result_board, ever_alive = next_board_state(board, classic_rules, {(0,2), (1,1)})

    assert result_board[1][1] == Config.DEAD

def test_next_board_state_corner_cell():
    """Corner cells should not consider out-of-bounds neighbors."""
    board = [
        [Config.DEAD, Config.ALIVE, Config.ALIVE],
        [Config.ALIVE, Config.DEAD, Config.DEAD],
        [Config.DEAD, Config.DEAD, Config.DEAD],
    ]

    result_board, ever_alive = next_board_state(board, classic_rules, {(0,1), (0,2), (1,0)})

    assert result_board[0][0] == Config.DEAD


def test_next_board_state_border_cell():
    """Edge cells should correctly count neighbors without index errors."""
    board = [
        [Config.DEAD, Config.DEAD, Config.DEAD],
        [Config.ALIVE, Config.ALIVE, Config.ALIVE],
        [Config.DEAD, Config.DEAD, Config.DEAD],
    ]

    result_board, ever_alive = next_board_state(board, classic_rules, {(1,0), (1,1), (1,2)})

    assert result_board[2][1] == Config.ALIVE
