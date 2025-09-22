from .utils import get_diff, load_data, get_monotonicity_violation_count, get_change_violation_count
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
    for row_series in dataset:
        if row_series.size <= 1:
            raise Warning("Skipping row. Report has less than 2 levels.")
            continue
        diffs = get_diff(row_series, absolute=False)
        abs_diffs = get_diff(row_series, absolute=True)
        num_violations = get_monotonicity_violation_count(diffs) + get_change_violation_count(abs_diffs, min_change=1, max_change=3)
        if num_violations == 0:
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
