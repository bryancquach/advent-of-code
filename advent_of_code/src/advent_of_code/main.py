import typer
from .day_01.cli import app as day01_app
from .day_02.cli import app as day02_app
from .day_03.cli import app as day03_app
from .day_04.cli import app as day04_app

app = typer.Typer(name="advent-of-code", help="Advent of Code Solutions CLI")

app.add_typer(day01_app, name="day-1", help="Run Day 1 solutions.")
app.add_typer(day02_app, name="day-2", help="Run Day 2 solutions.")
app.add_typer(day03_app, name="day-3", help="Run Day 3 solutions.")
app.add_typer(day04_app, name="day-4", help="Run Day 4 solutions.")


if __name__ == "__main__":
    app()
