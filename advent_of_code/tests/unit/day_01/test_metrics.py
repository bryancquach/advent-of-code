import pandas
import pytest
from advent_of_code.day_01.metrics import get_manhattan_dist, get_similarity_score


@pytest.fixture
def sample_data():
    # Example data from challenge description
    series1 = pandas.Series([1, 2, 3, 3, 3, 4]).astype(int)
    series2 = pandas.Series([3, 3, 3, 4, 5, 9]).astype(int)
    return series1, series2


def test_get_similarity_score(sample_data):
    expected_score = 31
    assert get_similarity_score(*sample_data) == expected_score


def test_get_manhattan_dist(sample_data):
    expected_distance = 11
    assert get_manhattan_dist(*sample_data) == expected_distance
