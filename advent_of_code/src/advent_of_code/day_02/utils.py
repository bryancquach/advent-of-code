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
