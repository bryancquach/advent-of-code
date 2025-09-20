import pandas


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
    df = pandas.read_table(file_path, sep="\t", header=None, dtype=int, na_filter=False)
    return df


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
