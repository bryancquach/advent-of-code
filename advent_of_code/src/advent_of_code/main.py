import typer
from .day_01.cli import app as day01_app

app = typer.Typer(name="advent-of-code", help="Advent of Code Solutions CLI")

app.add_typer(day01_app, name="day-1", help="Run Day 1 solutions.")

if __name__ == "__main__":
    app()
