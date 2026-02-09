from game_of_life import next_board_state, DEAD, ALIVE


def test_next_board_state_dead_cell_rule():
    """Test makes sure that dead cells with no live neighbors stay dead."""
    board = [
        [DEAD, DEAD, DEAD],
        [DEAD, DEAD, DEAD],
        [DEAD, DEAD, DEAD],
    ]

    result_board = next_board_state(board)

    assert result_board[1][1] == DEAD

def test_next_board_state_dead_cell_live_rule():
    """Test makes sure that dead cells with 3 live neighbors come alive."""
    board = [
        [ALIVE, DEAD, DEAD],
        [ALIVE, DEAD, DEAD],
        [ALIVE, DEAD, DEAD],
    ]

    result_board = next_board_state(board)

    assert result_board[1][1] == ALIVE


def test_next_board_state_blinker():
    """Test to makes sure that a Blinker works."""
    blinker_board = [
        [DEAD, ALIVE, DEAD],
        [DEAD, ALIVE, DEAD],
        [DEAD, ALIVE, DEAD],
    ]

    expected = [
        [DEAD, DEAD, DEAD],
        [ALIVE, ALIVE, ALIVE],
        [DEAD, DEAD, DEAD],
    ]

    assert next_board_state(blinker_board) == expected

def test_next_board_state_alive_cell_overpopulation():
    """Check that live cells die when they have more than 3 live neighbors"""
    board = [
        [DEAD, ALIVE, DEAD],
        [ALIVE, ALIVE, ALIVE],
        [DEAD, ALIVE, DEAD],
    ]

    result_board = next_board_state(board)

    assert result_board[1][1] == DEAD

def test_next_board_state_alive_cell_underpopulation():
    """Check that live cells die when they have less than 3 live neighbors"""
    board = [
        [DEAD, DEAD, ALIVE],
        [DEAD, ALIVE, DEAD],
        [DEAD, DEAD, DEAD],
    ]

    result_board = next_board_state(board)

    assert result_board[1][1] == DEAD

def test_next_board_state_corner_cell():
    """Corner cells should not consider out-of-bounds neighbors."""
    board = [
        [DEAD, ALIVE, ALIVE],
        [ALIVE, DEAD, DEAD],
        [DEAD, DEAD, DEAD],
    ]

    result_board = next_board_state(board)

    assert result_board[0][0] == DEAD


def test_next_board_state_border_cell():
    """Edge cells should correctly count neighbors without index errors."""
    board = [
        [DEAD, DEAD, DEAD],
        [ALIVE, ALIVE, ALIVE],
        [DEAD, DEAD, DEAD],
    ]

    result_board = next_board_state(board)

    assert result_board[2][1] == ALIVE
