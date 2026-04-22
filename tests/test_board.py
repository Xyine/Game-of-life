import pytest

from config.config import Config
from engine.board import BoardFile, build_from_coordinates, integrate_pattern


D = Config.DEAD
A = Config.ALIVE


def test_build_from_coordinates_creates_expected_board():
    data = BoardFile(
        format="coordinates",
        width=4,
        height=3,
        alive_cells=[[0, 1], [2, 3]],
    )

    board = build_from_coordinates(data)

    expected = [
        [D, A, D, D],
        [D, D, D, D],
        [D, D, D, A],
    ]

    assert board == expected


def test_build_from_coordinates_raises_for_out_of_bounds_cell():
    data = BoardFile(
        format="coordinates",
        width=3,
        height=3,
        alive_cells=[[3, 0]],
    )

    with pytest.raises(ValueError):
        build_from_coordinates(data)


def test_integrate_pattern_centers_pattern_correctly():
    pattern = [
        [A, A],
        [A, A],
    ]

    board = integrate_pattern(
        pattern=pattern,
        width=6,
        height=6,
        fill_mode="DEAD",
        placement="center",
    )

    expected = [
        [D, D, D, D, D, D],
        [D, D, D, D, D, D],
        [D, D, A, A, D, D],
        [D, D, A, A, D, D],
        [D, D, D, D, D, D],
        [D, D, D, D, D, D],
    ]

    assert board == expected


def test_integrate_pattern_raises_when_pattern_is_bigger_than_board():
    pattern = [
        [A, A, A],
        [A, A, A],
        [A, A, A],
    ]

    with pytest.raises(ValueError):
        integrate_pattern(
            pattern=pattern,
            width=2,
            height=2,
            fill_mode="DEAD",
            placement="topleft",
        )
