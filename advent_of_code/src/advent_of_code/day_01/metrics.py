from collections import Counter
import pandas


def get_manhattan_dist(
    series1: pandas.core.series.Series, series2: pandas.core.series.Series
) -> int:
    """Calculate Manhattan distance given two lists of integers.

    Args:
      series1 (pandas.core.series.Series): Series of integers.
      series2 (pandas.core.series.Series): Series of integers of same length as `series1`.

    Returns:
      int: The Manhattan distance between the two numeric series.
    """
    if series1.size != series2.size:
        raise ValueError("Input series must be of the same length.")
    return (series1 - series2).abs().sum()


def get_similarity_score(
    series1: pandas.core.series.Series, series2: pandas.core.series.Series
) -> int:
    """Calculate similarity score between two lists of integers.

    The similarity score is defined as a weighted sum of the items in the first series. For each
    item in the first series, a weight is defined as the frequency of the item within the second
    series.

    Args:
      series1 (pandas.core.series.Series): Series of integers.
      series2 (pandas.core.series.Series): Series of integers of same length as `series1`.

    Returns:
      int: Similarity score between the two numeric series.
    """
    if series1.size != series2.size:
        raise ValueError("Input series must be of the same length.")
    weights = Counter(series2)
    score = sum(item * weights.get(item, 0) for item in series1)
    return score
