import typer
from typing_extensions import Annotated

app = typer.Typer(help="Day 21: [Puzzle Title]")


@app.command()
def run_part1(
    data_file: Annotated[
        str, typer.Argument(..., help="Path to input file.")
    ],
):
    """Part 1 solution."""
    # TODO: Implement solution
    print("Part 1 not yet implemented")


@app.command()
def run_part2(
    data_file: Annotated[
        str, typer.Argument(..., help="Path to input file.")
    ],
):
    """Part 2 solution."""
    # TODO: Implement solution
    print("Part 2 not yet implemented")
