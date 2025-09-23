import pandas
import typer
from typing_extensions import Annotated
from .utils import (
    get_diff,
    load_data,
    get_series_combinations,
    get_change_violation_count,
    get_monotonicity_violation_count,
)


app = typer.Typer(help="Day 2: Red-Nosed Reports")


@app.command()
def run_part1(
    data_file: Annotated[
        str, typer.Argument(..., help="Path to a TSV file with rows of integers.")
    ],
):
    """Check if reports are monotonic and within change thresholds.

    This check only considers reports with no violations. The logic will break on reports with >0 violations.
    """
    dataset = load_data(data_file)
    safe_count = 0
    for row_series in dataset:
        if row_series.size <= 1:
            print("Warning: Skipping row. Report has less than 2 levels.")
            continue
        monotonicity_violations = get_monotonicity_violation_count(row_series)
        change_violations = get_change_violation_count(row_series, min_change=1, max_change=3)
        if monotonicity_violations == 0 and change_violations == 0:
            safe_count += 1
    print(f"Number of safe reports: {safe_count}")


@app.command()
def run_part2(
    data_file: Annotated[
        str, typer.Argument(..., help="Path to a TSV file with rows of integers.")
    ],
):
    """Check if reports are monotonic and within change thresholds assuming a 1 element tolerance.

    This check uses a brute force combinatorial approach to check if removing one element can make
    the report safe. This can become computationally expensive for reports with many levels.
    """
    dataset = load_data(data_file)
    global_safe_count = 0
    for row_series in dataset:
        if row_series.size <= 1:
            print("Warning: Skipping row. Report has less than 2 levels.")
            continue
        monotonicity_violations = get_monotonicity_violation_count(row_series)
        change_violations = get_change_violation_count(row_series, min_change=1, max_change=3)
        if monotonicity_violations == 0 and change_violations == 0:
            global_safe_count += 1
            continue  # no need to check combinations
        for _, row_combo in get_series_combinations(row_series, r=row_series.size - 1).iterrows():
            combo_monotonicity_violations = get_monotonicity_violation_count(
                pandas.Series(row_combo)
            )
            combo_change_violations = get_change_violation_count(
                pandas.Series(row_combo), min_change=1, max_change=3
            )
            if combo_monotonicity_violations == 0 and combo_change_violations == 0:
                global_safe_count += 1
                break  # no need to check for more safe combos
    print(f"Number of safe reports: {global_safe_count}")
