import numpy
import pandas
from numpy.typing import NDArray
from pathlib import Path


class Puzzle:
    """A word search puzzle data object.

    Holds the word search character matrix and provides methods for
    interacting with the puzzle.
    """

    def __init__(self, puzzle_file: Path):
        self.puzzle: pandas.DataFrame = self._load_puzzle(puzzle_file)

    def _load_puzzle(self, puzzle_file: Path) -> pandas.DataFrame:
        """Load the puzzle from a file into a DataFrame.

        Args:
            puzzle_file (Path): The path to the puzzle file.

        Returns:
            pandas.DataFrame: The loaded puzzle as a DataFrame of characters.
        """
        with open(puzzle_file, "r") as f:
            lines = f.readlines()
        data = [list(line.strip()) for line in lines]
        return pandas.DataFrame(data, dtype=str)

    def char_search(self, char: str) -> tuple[NDArray[numpy.int_], NDArray[numpy.int_]]:
        """Find all instances of a character in the puzzle.

        Args:
            char (str): The character for which to search.

        Returns:
            An array of row indices and a corresponding array of column indices.
        """
        if len(char) > 1:
            raise ValueError("'char' must be length 1.")
        rows, cols = numpy.where(self.puzzle == char)
        return rows, cols

    def _get_north(self, row_index: int, col_index: int, length: int) -> str:
        """Get the puzzle values moving northward from the start position.

        Only returns the values if the entire word fits within the puzzle boundaries.

        Args:
            row_index (int): The starting row index.
            col_index (int): The starting col_index.
            length (int): The number of values to retrieve.

        Returns:
            The puzzle values as a string.
        """
        if row_index < 0 or row_index >= self.puzzle.shape[0]:
            raise IndexError("Row index is outside the puzzle boundaries.")
        if col_index < 0 or col_index >= self.puzzle.shape[1]:
            raise IndexError("Column index is outside the puzzle boundaries.")
        if length <= 0:
            return ""
        if row_index - length + 1 < 0:
            return ""
        return self.puzzle.iloc[row_index - length + 1 : row_index + 1, col_index][::-1].str.cat(
            sep=""
        )

    def _get_south(self, row_index: int, col_index: int, length: int) -> str:
        """Get the puzzle values moving southward from the start position.

        Only returns the values if the entire word fits within the puzzle boundaries.

        Args:
            row_index (int): The starting row index.
            col_index (int): The starting col_index.
            length (int): The number of values to retrieve.

        Returns:
            The puzzle values as a string.
        """
        if row_index < 0 or row_index >= self.puzzle.shape[0]:
            raise IndexError("Row index is outside the puzzle boundaries.")
        if col_index < 0 or col_index >= self.puzzle.shape[1]:
            raise IndexError("Column index is outside the puzzle boundaries.")
        if length <= 0:
            return ""
        if row_index + length > self.puzzle.shape[0]:
            return ""
        return self.puzzle.iloc[row_index : row_index + length, col_index].str.cat(sep="")

    def _get_east(self, row_index: int, col_index: int, length: int) -> str:
        """Get the puzzle values moving eastward from the start position.

        Only returns the values if the entire word fits within the puzzle boundaries.

        Args:
            row_index (int): The starting row index.
            col_index (int): The starting col_index.
            length (int): The number of values to retrieve.

        Returns:
            The puzzle values as a string.
        """
        if row_index < 0 or row_index >= self.puzzle.shape[0]:
            raise IndexError("Row index is outside the puzzle boundaries.")
        if col_index < 0 or col_index >= self.puzzle.shape[1]:
            raise IndexError("Column index is outside the puzzle boundaries.")
        if length <= 0:
            return ""
        if col_index + length > self.puzzle.shape[1]:
            return ""
        return self.puzzle.iloc[row_index, col_index : col_index + length].str.cat(sep="")

    def _get_west(self, row_index: int, col_index: int, length: int) -> str:
        """Get the puzzle values moving westward from the start position.

        Only returns the values if the entire word fits within the puzzle boundaries.

        Args:
            row_index (int): The starting row index.
            col_index (int): The starting col_index.
            length (int): The number of values to retrieve.

        Returns:
            The puzzle values as a string.
        """
        if row_index < 0 or row_index >= self.puzzle.shape[0]:
            raise IndexError("Row index is outside the puzzle boundaries.")
        if col_index < 0 or col_index >= self.puzzle.shape[1]:
            raise IndexError("Column index is outside the puzzle boundaries.")
        if length <= 0:
            return ""
        if col_index - length + 1 < 0:
            return ""
        return self.puzzle.iloc[row_index, col_index - length + 1 : col_index + 1][::-1].str.cat(
            sep=""
        )

    def _get_northeast(self, row_index: int, col_index: int, length: int) -> str:
        """Get the puzzle values moving northeastward from the start position.

        Only returns the values if the entire word fits within the puzzle boundaries.

        Args:
            row_index (int): The starting row index.
            col_index (int): The starting col_index.
            length (int): The number of values to retrieve.

        Returns:
            The puzzle values as a string.
        """
        if row_index < 0 or row_index >= self.puzzle.shape[0]:
            raise IndexError("Row index outside the puzzle boundaries.")
        if col_index < 0 or col_index >= self.puzzle.shape[1]:
            raise IndexError("Column index outside the puzzle boundaries.")
        if length <= 0:
            return ""
        if row_index - length + 1 < 0 or col_index + length > self.puzzle.shape[1]:
            return ""
        row_indices = [row_index - i for i in range(length)]
        col_indices = [col_index + i for i in range(length)]
        char_list = [str(self.puzzle.iloc[row, col]) for row, col in zip(row_indices, col_indices)]
        return "".join(char_list)

    def _get_northwest(self, row_index: int, col_index: int, length: int) -> str:
        """Get the puzzle values moving northwestward from the start position.

        Only returns the values if the entire word fits within the puzzle boundaries.

        Args:
            row_index (int): The starting row index.
            col_index (int): The starting col_index.
            length (int): The number of values to retrieve.

        Returns:
            The puzzle values as a string.
        """
        if row_index < 0 or row_index >= self.puzzle.shape[0]:
            raise IndexError("Row index outside the puzzle boundaries.")
        if col_index < 0 or col_index >= self.puzzle.shape[1]:
            raise IndexError("Column index outside the puzzle boundaries.")
        if length <= 0:
            return ""
        if row_index - length + 1 < 0 or col_index - length + 1 < 0:
            return ""
        row_indices = [row_index - i for i in range(length)]
        col_indices = [col_index - i for i in range(length)]
        char_list = [str(self.puzzle.iloc[row, col]) for row, col in zip(row_indices, col_indices)]
        return "".join(char_list)

    def _get_southeast(self, row_index: int, col_index: int, length: int) -> str:
        """Get the puzzle values moving southeastward from the start position.

        Only returns the values if the entire word fits within the puzzle boundaries.

        Args:
            row_index (int): The starting row index.
            col_index (int): The starting col_index.
            length (int): The number of values to retrieve.

        Returns:
            The puzzle values as a string.
        """
        if row_index < 0 or row_index >= self.puzzle.shape[0]:
            raise IndexError("Row index outside the puzzle boundaries.")
        if col_index < 0 or col_index >= self.puzzle.shape[1]:
            raise IndexError("Column index outside the puzzle boundaries.")
        if length <= 0:
            return ""
        if row_index + length > self.puzzle.shape[0] or col_index + length > self.puzzle.shape[1]:
            return ""
        row_indices = [row_index + i for i in range(length)]
        col_indices = [col_index + i for i in range(length)]
        char_list = [str(self.puzzle.iloc[row, col]) for row, col in zip(row_indices, col_indices)]
        return "".join(char_list)

    def _get_southwest(self, row_index: int, col_index: int, length: int) -> str:
        """Get the puzzle values moving southwestward from the start position.

        Only returns the values if the entire word fits within the puzzle boundaries.

        Args:
            row_index (int): The starting row index.
            col_index (int): The starting col_index.
            length (int): The number of values to retrieve.

        Returns:
            The puzzle values as a string.
        """
        if length <= 0:
            return ""
        if row_index < 0 or row_index >= self.puzzle.shape[0]:
            raise IndexError("Row index outside the puzzle boundaries.")
        if col_index < 0 or col_index >= self.puzzle.shape[1]:
            raise IndexError("Column index outside the puzzle boundaries.")
        if length <= 0:
            return ""
        if row_index + length > self.puzzle.shape[0] or col_index - length + 1 < 0:
            return ""
        row_indices = [row_index + i for i in range(length)]
        col_indices = [col_index - i for i in range(length)]
        char_list = [str(self.puzzle.iloc[row, col]) for row, col in zip(row_indices, col_indices)]
        return "".join(char_list)

    def get_word_count(self, word: str, row_index: int, col_index: int) -> int:
        """Tally how often a word exists in the puzzle in any direction from the specified position.

        Row and column positions are zero-indexed.

        Args:
            word (str): The word to search for.
            row_index (int): The starting row index.
            col_index (int): The starting col_index.

        Returns:
            int: The count of occurrences of the word.
        """
        # Check all 8 directions
        total = 0
        for direction in [
            self._get_north,
            self._get_northeast,
            self._get_east,
            self._get_southeast,
            self._get_south,
            self._get_southwest,
            self._get_west,
            self._get_northwest,
        ]:
            if word == direction(row_index, col_index, len(word)):
                total += 1
        return total

    def get_x_mas_count(self) -> int:
        """Count the total occurrences of X-shaped "MAS" patterns in the puzzle.

        Returns:
            int: The total count of X-shaped "MAS" occurrences.
        """
        row_indices, col_indices = self.char_search("A")
        # Prune indices that cannot form an X shape (on the edges)
        valid_indices = [
            (row, col)
            for row, col in zip(row_indices, col_indices)
            if 0 < row < self.puzzle.shape[0] - 1 and 0 < col < self.puzzle.shape[1] - 1
        ]
        total = 0
        for row, col in valid_indices:
            # Look for only X's (not crosses)
            if (
                self._get_northeast(row + 1, col - 1, 3) == "MAS"
                or self._get_southwest(row - 1, col + 1, 3) == "MAS"
            ) and (
                self._get_northwest(row + 1, col + 1, 3) == "MAS"
                or self._get_southeast(row - 1, col - 1, 3) == "MAS"
            ):
                total += 1
        return total
