import pandas
import typer
from pathlib import Path
from typing_extensions import Annotated
from .utils import Puzzle

app = typer.Typer(help="Day 4: Ceres Search")


@app.command()
def run_part1(
    data_file: Annotated[
        str, typer.Argument(..., help="Path to a fixed-width file with an input puzzle.")
    ],
):
    """Count number of "XMAS" occurrences."""
    puzzle = Puzzle(Path(data_file))
    row_indices, col_indices = puzzle.char_search("X")
    count = sum(
        puzzle.get_word_count("XMAS", row, col) for row, col in zip(row_indices, col_indices)
    )
    typer.echo(f"Number of 'XMAS' occurrences: {count}")


@app.command()
def run_part2(
    data_file: Annotated[
        str, typer.Argument(..., help="Path to a fixed-width file with an input puzzle.")
    ],
):
    """Count number of X-shaped 'MAS' occurrences."""
    puzzle = Puzzle(Path(data_file))
    count = puzzle.get_x_mas_count()
    typer.echo(f"Number of X-shaped 'MAS' occurrences: {count}")
