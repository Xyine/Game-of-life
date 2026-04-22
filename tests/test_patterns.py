from engine.patterns import detect_patterns


def test_detect_patterns_finds_block():
    board = [
        [0, 0, 0, 0],
        [0, 1, 1, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0],
    ]

    patterns = detect_patterns(board)

    assert len(patterns) == 1
    assert patterns[0].name == "block"


def test_detect_patterns_finds_blinker():
    board = [
        [0, 0, 0],
        [1, 1, 1],
        [0, 0, 0],
    ]

    patterns = detect_patterns(board)

    assert len(patterns) == 1
    assert patterns[0].name == "blinker"
