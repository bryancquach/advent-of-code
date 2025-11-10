import pandas
import typer
from pathlib import Path
from typing_extensions import Annotated
from .utils import Puzzle

app = typer.Typer(help="Day 4: Ceres Search")


@app.command()
def run_part1(
    data_file: Annotated[
        str, typer.Argument(..., help="Path to a non-delimited file with an input puzzle.")
    ],
):
    """Count number of "XMAS" occurrences."""
    puzzle = Puzzle(Path(data_file))
    row_indices, col_indices = puzzle.char_search("X")
    count = sum(puzzle.get_word_count("XMAS", row, col) for row, col in zip(row_indices, col_indices))
    typer.echo(f"Number of 'XMAS' occurrences: {count}")


@app.command()
def run_part2(
    data_file: Annotated[
        str, typer.Argument(..., help="Path to a TSV file.")
    ],
):
    """Part 2 (not yet implemented)."""
    #TODO: Implement part 2
    pass
