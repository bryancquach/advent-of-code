import pandas
import pytest
from advent_of_code.day_01.distance_metrics import get_manhattan_dist

def test_get_manhattan_dist():
  # Example data from challenge description
  series1 = pandas.Series([1, 2, 3, 3, 3, 4])
  series2 = pandas.Series([3, 3, 3, 4, 5, 9])
  expected_distance = 11.0
  assert get_manhattan_dist(series1, series2) == expected_distance