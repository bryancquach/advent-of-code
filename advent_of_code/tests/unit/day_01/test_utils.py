import pandas
import pytest
from advent_of_code.day_01.utils import get_manhattan_dist, get_similarity_score


@pytest.fixture
def sample_data():
    # Example data from challenge description but with mismatched indices
    series1 = pandas.Series([1, 2, 3, 3, 3, 4], index=["A", "B", "C", "D", "E", "F"]).astype(int)
    series2 = pandas.Series([3, 3, 3, 4, 5, 9], index=["A", "C", "D", "B", "F", "E"]).astype(int)
    return series1, series2


@pytest.fixture
def invalid_data():
    # Data with non-integer types
    series1 = pandas.Series([1, 2, 3, 3, 3, 4], index=["A", "B", "C", "D", "E", "F"]).astype(int)
    series2 = pandas.Series(["3", "3", "3", "4", "5", "9"], index=["A", "C", "D", "B", "F", "E"])
    return series1, series2


def test_get_similarity_score(sample_data, invalid_data):
    expected_score = 31
    assert get_similarity_score(*sample_data) == expected_score
    with pytest.raises(ValueError):
        get_similarity_score(*invalid_data)


def test_get_manhattan_dist(sample_data, invalid_data):
    expected_distance = 11
    assert get_manhattan_dist(*sample_data) == expected_distance
    with pytest.raises(ValueError):
        get_manhattan_dist(*invalid_data)
