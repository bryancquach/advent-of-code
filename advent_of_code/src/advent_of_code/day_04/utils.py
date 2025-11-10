import numpy
import pandas
from numpy.typing import NDArray

class Puzzle:
    """A word search puzzle data object.

    Holds the word search character matrix and provides methods for
    interacting with the puzzle.
    """
    def __init__(self, puzzle: pandas.DataFrame):
        self.puzzle = puzzle

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

        Args:
            row_index (int): The starting row index.
            col_index (int): The starting col_index.
            length (int): The number of values to retrieve.

        Returns:
            The puzzle values as a string.
        """
        if length <= 0:
            return ""
        if row_index - length < 0 or row_index >= self.puzzle.shape[0]:
            raise IndexError("Row index and length combined are outside the puzzle boundaries.")
        if col_index < 0 or col_index >= self.puzzle.shape[1]:
            raise IndexError("Column index is outside the puzzle boundaries.")
        return self.puzzle.iloc[row_index - length + 1:row_index + 1, col_index].to_string(index=False, header=False)
        
    def _get_south(self, row_index: int, col_index: int, length: int) -> str:
        """Get the puzzle values moving southward from the start position.

        Args:
            row_index (int): The starting row index.
            col_index (int): The starting col_index.
            length (int): The number of values to retrieve.
        
        Returns:
            The puzzle values as a string.
        """
        if length <= 0:
            return ""
        if row_index + length > self.puzzle.shape[0] or row_index < 0:
            raise IndexError("Row index and length combined are outside the puzzle boundaries.")
        if col_index < 0 or col_index >= self.puzzle.shape[1]:
            raise IndexError("Column index is outside the puzzle boundaries.")
        return self.puzzle.iloc[row_index:row_index + length, col_index].to_string(index=False, header=False)
    
    def _get_east(self, row_index: int, col_index: int, length: int) -> str:
        """Get the puzzle values moving eastward from the start position.

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
            raise IndexError("Row index is outside the puzzle boundaries.")
        if col_index + length > self.puzzle.shape[1] or col_index < 0:
            raise IndexError("Column index and length combined are outside the puzzle boundaries.")
        return self.puzzle.iloc[row_index, col_index:col_index + length].to_string(index=False, header=False)
    
    def _get_west(self, row_index: int, col_index: int, length: int) -> str:
        """Get the puzzle values moving westward from the start position.

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
            raise IndexError("Row index is outside the puzzle boundaries.")
        if col_index - length < 0 or col_index >= self.puzzle.shape[1]:
            raise IndexError("Column index and length combined are outside the puzzle boundaries.")
        return self.puzzle.iloc[row_index, col_index - length + 1:col_index + 1].to_string(index=False, header=False)
    

    def _get_northeast(self, row_index: int, col_index: int, length: int) -> str:
        """Get the puzzle values moving northeastward from the start position.

        Args:
            row_index (int): The starting row index.
            col_index (int): The starting col_index.
            length (int): The number of values to retrieve.

        Returns:
            The puzzle values as a string.
        """
        if length <= 0:
            return ""
        if row_index - length < 0 or row_index >= self.puzzle.shape[0]:
            raise IndexError("Row index and length combined are outside the puzzle boundaries.")
        if col_index + length > self.puzzle.shape[1] or col_index < 0:
            raise IndexError("Column index and length combined are outside the puzzle boundaries.")
        row_indices = [row_index - i for i in range(length)]
        col_indices = [col_index + i for i in range(length)]
        return self.puzzle.iloc[row_indices, col_indices].to_string(index=False, header=False)

    def _get_northwest(self, row_index: int, col_index: int, length: int) -> str:
        """Get the puzzle values moving northwestward from the start position.

        Args:
            row_index (int): The starting row index.
            col_index (int): The starting col_index.
            length (int): The number of values to retrieve.
        
        Returns:
            The puzzle values as a string.
        """
        if length <= 0:
            return ""
        if row_index - length < 0 or row_index >= self.puzzle.shape[0]:
            raise IndexError("Row index and length combined are outside the puzzle boundaries.")
        if col_index - length < 0 or col_index >= self.puzzle.shape[1]:
            raise IndexError("Column index and length combined are outside the puzzle boundaries.")
        row_indices = [row_index - i for i in range(length)]
        col_indices = [col_index - i for i in range(length)]
        return self.puzzle.iloc[row_indices, col_indices].to_string(index=False, header=False)
    
    def _get_southeast(self, row_index: int, col_index: int, length: int) -> str:
        """Get the puzzle values moving southeastward from the start position.

        Args:
            row_index (int): The starting row index.
            col_index (int): The starting col_index.
            length (int): The number of values to retrieve.

        Returns:
            The puzzle values as a string.
        """
        if length <= 0:
            return ""
        if row_index + length > self.puzzle.shape[0] or row_index < 0:
            raise IndexError("Row index and length combined are outside the puzzle boundaries.")
        if col_index + length > self.puzzle.shape[1] or col_index < 0:
            raise IndexError("Column index and length combined are outside the puzzle boundaries.")
        row_indices = [row_index + i for i in range(length)]
        col_indices = [col_index + i for i in range(length)]
        return self.puzzle.iloc[row_indices, col_indices].to_string(index=False, header=False)
    
    def _get_southwest(self, row_index: int, col_index: int, length: int) -> str:
        """Get the puzzle values moving southwestward from the start position.

        Args:
            row_index (int): The starting row index.
            col_index (int): The starting col_index.
            length (int): The number of values to retrieve.
        
        Returns:
            The puzzle values as a string.
        """
        if length <= 0:
            return ""
        if row_index + length > self.puzzle.shape[0] or row_index < 0:
            raise IndexError("Row index and length combined are outside the puzzle boundaries.")
        if col_index - length < 0 or col_index >= self.puzzle.shape[1]:
            raise IndexError("Column index and length combined are outside the puzzle boundaries.")
        row_indices = [row_index + i for i in range(length)]
        col_indices = [col_index - i for i in range(length)]
        return self.puzzle.iloc[row_indices, col_indices].to_string(index=False, header=False)

    def check_word(self, word: str, row_index: int, col_index: int) -> bool:
        """Check if a word exists in the puzzle in any direction from the specified position.

        Row and column positions are zero-indexed.

        Args:
            word (str): The word to search for.
            row_index (int): The starting row index.
            col_index (int): The starting col_index.

        Returns:
            bool: True if the word is found, False otherwise.
        """
        # Check all 8 directions
        for direction in [self._get_north, self._get_northeast, self._get_east, self._get_southeast,
                          self._get_south, self._get_southwest, self._get_west, self._get_northwest]:
            if word == direction(row_index, col_index, len(word)):
                return True
        return False