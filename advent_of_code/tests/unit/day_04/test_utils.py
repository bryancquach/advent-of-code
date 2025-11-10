from advent_of_code.day_04.utils import Puzzle
import pandas
import pathlib
import pytest

SCRIPT_DIR = pathlib.Path(__file__).parent.resolve()


@pytest.fixture(scope="session")
def file_paths():
    return {
        "example_puzzle": f"{SCRIPT_DIR}/data/example_data.tsv",  # Example data from challenge description
        "no_xmas_puzzle": f"{SCRIPT_DIR}/data/no_xmas_data.tsv",  # File without any 'XMAS' occurrences
        "empty_puzzle": f"{SCRIPT_DIR}/data/empty_file.tsv",  # Empty file
    }


@pytest.fixture(scope="session")
def puzzle_sets(file_paths):
    puzzles = {"example_puzzle": None, "no_xmas_puzzle": None, "empty_puzzle": None}
    puzzles["example_puzzle"] = Puzzle(file_paths["example_puzzle"])
    puzzles["no_xmas_puzzle"] = Puzzle(file_paths["no_xmas_puzzle"])
    puzzles["empty_puzzle"] = Puzzle(file_paths["empty_puzzle"])
    data = pandas.DataFrame(
        [
            ["A", "B", "C"],
            ["D", "E", "F"],
            ["G", "H", "I"],
            ["J", "K", "L"],
            ["M", "N", "O"],
        ]
    )
    puzzle = Puzzle.__new__(Puzzle)
    puzzle.puzzle = data
    puzzles["abc_puzzle"] = puzzle
    return puzzles


def test_char_search(puzzle_sets):
    puzzle = puzzle_sets["example_puzzle"]
    row_indices, col_indices = puzzle.char_search("X")
    assert len(row_indices) > 0
    assert len(col_indices) > 0
    for row, col in zip(row_indices, col_indices):
        assert puzzle.puzzle.iat[row, col] == "X"

    puzzle = puzzle_sets["no_xmas_puzzle"]
    row_indices, col_indices = puzzle.char_search("X")
    assert len(row_indices) == 0
    assert len(col_indices) == 0

def test_get_north(puzzle_sets):
    puzzle = puzzle_sets["abc_puzzle"]
    assert puzzle._get_north(4, 0, 5) == "MJGDA"
    assert puzzle._get_north(0, 0, 3) == ""
    with pytest.raises(IndexError):
        puzzle._get_north(0, 5, 2)


def test_get_south(puzzle_sets):
    puzzle = puzzle_sets["abc_puzzle"]
    assert puzzle._get_south(4, 0, 2) == ""
    assert puzzle._get_south(0, 0, 5) == "ADGJM"
    with pytest.raises(IndexError):
        puzzle._get_south(10, 5, 2)


def test_get_east(puzzle_sets):
    puzzle = puzzle_sets["abc_puzzle"]
    assert puzzle._get_east(0, 0, 3) == "ABC"
    assert puzzle._get_east(4, 2, 3) == ""
    with pytest.raises(IndexError):
        puzzle._get_east(2, 10, 2)


def test_get_west(puzzle_sets):
    puzzle = puzzle_sets["abc_puzzle"]
    assert puzzle._get_west(0, 2, 3) == "CBA"
    assert puzzle._get_west(4, 0, 3) == ""
    with pytest.raises(IndexError):
        puzzle._get_west(2, -1, 2)


def test_get_northeast(puzzle_sets):
    puzzle = puzzle_sets["abc_puzzle"]
    assert puzzle._get_northeast(4, 0, 3) == "MKI"
    assert puzzle._get_northeast(0, 2, 4) == ""
    with pytest.raises(IndexError):
        puzzle._get_northeast(0, 10, 2)


def test_get_northwest(puzzle_sets):
    puzzle = puzzle_sets["abc_puzzle"]
    assert puzzle._get_northwest(4, 2, 3) == "OKG"
    assert puzzle._get_northwest(0, 0, 3) == ""
    with pytest.raises(IndexError):
        puzzle._get_northwest(0, -1, 2)


def test_get_southeast(puzzle_sets):
    puzzle = puzzle_sets["abc_puzzle"]
    assert puzzle._get_southeast(0, 0, 3) == "AEI"
    assert puzzle._get_southeast(2, 2, 4) == ""
    with pytest.raises(IndexError):
        puzzle._get_southeast(10, 0, 2)


def test_get_southwest(puzzle_sets):
    puzzle = puzzle_sets["abc_puzzle"]
    assert puzzle._get_southwest(0, 2, 3) == "CEG"
    assert puzzle._get_southwest(2, 0, 4) == ""
    with pytest.raises(IndexError):
        puzzle._get_southwest(10, -1, 2)

def test_get_word_count(puzzle_sets):
    puzzle = puzzle_sets["example_puzzle"]
    row_indices, col_indices = puzzle.char_search("X")
    found_count = 0
    for row, col in zip(row_indices, col_indices):
        found_count += puzzle.get_word_count("XMAS", row, col)
    assert found_count == 18, f"The word 'XMAS' was found {found_count}/18 times."
