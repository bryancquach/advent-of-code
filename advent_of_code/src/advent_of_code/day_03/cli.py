import typer
from typing_extensions import Annotated
from .utils import MulStateMachine

app = typer.Typer(help="Day 3: Mull It Over")


@app.command()
def run_part1(
    data_file: Annotated[
        str, typer.Argument(..., help="Path to a TSV file with character stream.")
    ],
):
    """Process data as a stream to parse and perform arithmetic operations."""
    state_machine = MulStateMachine(disable_dont=True)
    try:
        with open(data_file, "r", encoding="utf-8") as f:
            while True:
                char = f.read(1)
                if not char:
                    break
                state_machine.process_event(char)
    except FileNotFoundError:
        print(f"Error: The file '{data_file}' was not found.")
    print(f"Final value: {state_machine.mul}")


@app.command()
def run_part2(
    data_file: Annotated[
        str, typer.Argument(..., help="Path to a TSV file with character stream.")
    ],
):
    """Extension of Part 1.

    Adds support for toggling between 'do()' and 'don't()' modes to enable or disable arithmetic
    operations.
    """
    state_machine = MulStateMachine(disable_dont=False)
    try:
        with open(data_file, "r", encoding="utf-8") as f:
            while True:
                char = f.read(1)
                if not char:
                    break
                state_machine.process_event(char)
    except FileNotFoundError:
        print(f"Error: The file '{data_file}' was not found.")
    print(f"Final value: {state_machine.mul}")
