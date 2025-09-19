from .distance_metrics import get_manhattan_dist
import pandas
import typer
from typing_extensions import Annotated

app = typer.Typer(help="Day 1: Historian Hysteria")


@app.command()
def run_part1(
    data_file: Annotated[
        str, typer.Argument(..., help="Path to a TSV file for a two-column numeric matrix.")
    ],
    is_sorted: Annotated[
        bool,
        typer.Option(
            "--sorted", help="Flag indicating the input data is already sorted.", is_flag=True
        ),
    ] = False,
):
    """Calculate the Manhattan distance between two numeric series from a TSV file."""
    df = pandas.read_table(data_file, sep="\t", header=None)
    if df.shape[1] != 2:
        print("Error: Data file must contain exactly two columns.")
        raise typer.Exit(code=1)
    series1 = df.iloc[:, 0].copy()
    series2 = df.iloc[:, 1].copy()
    if not is_sorted:
        series1.sort_values(inplace=True, ignore_index=True)
        series2.sort_values(inplace=True, ignore_index=True)
    distance = get_manhattan_dist(series1, series2)
    print(f"Manhattan distance: {distance}")
