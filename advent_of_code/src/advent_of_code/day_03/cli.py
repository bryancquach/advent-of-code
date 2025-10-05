import typer
from typing_extensions import Annotated
from .utils import Muller

app = typer.Typer(help="Day 2: Red-Nosed Reports")


@app.command()
def run_part1(
    data_file: Annotated[
        str, typer.Argument(..., help="Path to a TSV file with character stream.")
    ],
):
    """Process data as a stream to parse and perform arithmetic operations."""
    muller = Muller()
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            while True:
                char = f.read(1)
                if not char:
                    break
                muller.process_event(char)
    except FileNotFoundError:
        print(f"Error: The file '{data_file}' was not found.")
    print(f"Final value: {muller.get_mul()}")


@app.command()
def run_part2(
    data_file: Annotated[
        str, typer.Argument(..., help="Path to a TSV file.")
    ],
):
    """Placeholder for Part 2 functionality.
    """
    pass