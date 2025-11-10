from advent_of_code.day_04.utils import Puzzle
import pandas
import pytest

SCRIPT_DIR = pathlib.Path(__file__).parent.resolve()


@pytest.fixture
def file_paths():
    return {
        "example_puzzle": f"{SCRIPT_DIR}/data/example_data.tsv",  # Example data from challenge description
        "no_xmas_puzzle": f"{SCRIPT_DIR}/data/no_xmas_data.tsv",  # File without any 'XMAS' occurrences
    }


@pytest.fixture(scope="session")
def part1_puzzles(file_paths):
    puzzles = {"example_puzzle": None, "no_xmas_puzzle": None}
    puzzles["example_puzzle"] = Puzzle(pandas.read_csv(file_paths["example_puzzle"], sep="", header=None))
    puzzles["no_xmas_puzzle"] = Puzzle(pandas.read_csv(file_paths["no_xmas_puzzle"], sep="", header=None))
    return puzzles

def test_char_search(part1_puzzles):
    puzzle = part1_puzzles["example_puzzle"]
    row_indices, col_indices = puzzle.char_search("X")
    assert len(row_indices) > 0
    assert len(col_indices) > 0
    for row, col in zip(row_indices, col_indices):
        assert puzzle.puzzle.iat[row, col] == "X"

    puzzle = part1_puzzles["no_xmas_puzzle"]
    row_indices, col_indices = puzzle.char_search("X")
    assert len(row_indices) == 0
    assert len(col_indices) == 0
