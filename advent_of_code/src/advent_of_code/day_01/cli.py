from .distance_metrics import get_manhattan_dist
import pandas
import typer
from typing_extensions import Annotated

app = typer.Typer(help="Day 1: Historian Hysteria")


def load_data(file_path: str) -> pandas.DataFrame:
    """Load a TSV file into a pandas DataFrame.

    Args:
      file_path (str): Path to the TSV file.

    Returns:
      pandas.DataFrame: DataFrame containing the data from the TSV file.
    """
    if file_path is None or not isinstance(file_path, str) or file_path.strip() == "":
        print("Error: A valid file path must be provided.")
        raise typer.Exit(code=1)
    df = pandas.read_table(file_path, sep="\t", header=None, dtype=int)
    if df.shape[1] != 2:
        print("Error: Data file must contain exactly two columns.")
        raise typer.Exit(code=1)
    return df


@app.command()
def run_part1(
    data_file: Annotated[
        str, typer.Argument(..., help="Path to a TSV file for a two-column integer matrix.")
    ],
    is_sorted: Annotated[
        bool,
        typer.Option(
            "--sorted", help="Flag indicating the input data is already sorted.", is_flag=True
        ),
    ] = False,
):
    """Calculate the Manhattan distance between two integer series from a TSV file."""
    dataset = load_data(data_file)
    series1 = dataset.iloc[:, 0].copy(deep=True)
    series2 = dataset.iloc[:, 1].copy(deep=True)
    if not is_sorted:
        series1.sort_values(inplace=True, ignore_index=True)
        series2.sort_values(inplace=True, ignore_index=True)
    distance = get_manhattan_dist(series1, series2)
    print(f"Manhattan distance: {distance}")
