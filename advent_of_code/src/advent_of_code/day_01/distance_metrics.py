import pandas


def get_manhattan_dist(
    series1: pandas.core.series.Series, series2: pandas.core.series.Series
) -> float:
    """Calculate Manhattan distance given two lists of numbers.

    Args:
      series1 (pandas.core.series.Series): Series of numbers.
      series2 (pandas.core.series.Series): Series of numbers of same length as `series1`.

    Returns:
      float: The Manhattan distance between the two numeric series.
    """
    if series1.size != series2.size:
        raise ValueError("Input series must be of the same length.")
    return (series1 - series2).abs().sum().astype(float)
