import pandas
import typer

def load_data(file_path: str) -> list[pandas.core.series.Series]:
    """Load a TSV file into a pandas DataFrame.

    Args:
        file_path (str): Path to the TSV file.

    Returns:
        list: list of pandas.Series containing the data from the TSV file.
    """
    data = list()
    if file_path is None or not isinstance(file_path, str) or file_path.strip() == "":
        print("Error: A valid file path must be provided.")
        raise typer.Exit(code=1)
    with open(file_path, 'r') as fh:
        if fh.read().strip() == "":
            print("Error: The provided file is empty.")
            raise typer.Exit(code=1)
    with open(file_path, 'r') as fh:
        for line in fh:
            line = line.strip()
            if line:
                try:
                    series = pandas.Series([int(x) for x in line.split('\t')])
                    data.append(series)
                except ValueError:
                    print(f"Error: Non-integer value found in line: {line}")
                    raise typer.Exit(code=1)
            else:
                raise Warning("Skipping empty line.")
    return data


def get_diff(series: pandas.Series, absolute: bool = False) -> pandas.Series:
    """Calculate the difference between consecutive elements in a series.

    Args:
        series (pandas.Series): Input series of integers.
        absolute (bool): If True, return absolute values of the differences.
    Returns:
        pandas.Series: Series of differences.
    """
    if absolute:
        return series.diff()[1:].abs().astype(int).reset_index(drop=True)
    return series.diff()[1:].astype(int).reset_index(drop=True)


def get_monotonicity_violation_count(series_diff: pandas.Series) -> int:
    """Tally number of elements violating a monotonicity assumption.

    Args:
        series_diff (pandas.Series): Series of integers representing differences between consecutive elements.
    
    Returns:
        int: Number of elements that violate monotonicity.
    """
    if len(series_diff) == 0:
        return 0
    
    # Find first non-zero element to establish direction
    for i in range(len(series_diff)):
        if series_diff.iloc[i] != 0:
            if series_diff.iloc[i] > 0:
                return (series_diff < 0).sum()
            else:
                return (series_diff > 0).sum()
    # All elements are zero
    return 0


def get_change_violation_count(series_diff: pandas.Series, min_change: int = 1, max_change: int = 3) -> int:
    """Tally number of elements violating change rate thresholds.

    Args:
        series (pandas.Series): Series of integers representing differences between consecutive elements.
        min_change (int): Minimum allowed absolute change.
        max_change (int): Maximum allowed absolute change.
    
    Returns:
        int: Number of elements that violate change rate thresholds.
    """
    if min_change < 0 or max_change < 0 or min_change > max_change:
        raise ValueError("Invalid change thresholds provided.")
    violations = 0
    violations += (series_diff < min_change).sum()
    violations += (series_diff > max_change).sum()
    return violations