from .utils import get_diff, load_data
import pandas
import typer
from typing_extensions import Annotated

app = typer.Typer(help="Day 2: Red-Nosed Reports")


@app.command()
def run_part1(
    data_file: Annotated[
        str, typer.Argument(..., help="Path to a TSV file for a two-column integer matrix.")
    ],
):
    """Check if reports are monotonic and within change thresholds."""
    dataset = load_data(data_file)
    safe_count = 0
    for _, row_series in dataset.iterrows():
        is_monotonic = row_series.is_monotonic_increasing or row_series.is_monotonic_decreasing
        if not is_monotonic:
            continue
        change_rate = get_diff(row_series, absolute=True)
        max_change = change_rate.max()
        min_change = change_rate.min()
        is_within_threshold = min_change >= 1 and max_change <= 3
        if not is_within_threshold:
            continue
        # Only increment if both conditions are met
        safe_count += 1
    print(f"Number of safe reports: {safe_count}")


@app.command()
def run_part2(
    data_file: Annotated[
        str, typer.Argument(..., help="Path to a TSV file for a two-column integer matrix.")
    ],
):
    """TODO: Implement part 2."""
    pass
