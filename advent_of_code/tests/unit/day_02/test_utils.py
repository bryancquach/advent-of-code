from advent_of_code.day_02.utils import (
    get_diff,
    load_data,
    get_series_combinations,
    get_change_violation_count,
    get_monotonicity_violation_count,
)
import itertools
import pandas
import pathlib
import pytest
import typer

SCRIPT_DIR = pathlib.Path(__file__).parent.resolve()


@pytest.fixture
def file_paths():
    return [
        f"{SCRIPT_DIR}/data/example_data.tsv",  # Example data from challenge description
        f"{SCRIPT_DIR}/data/empty_file.tsv",
        f"{SCRIPT_DIR}/data/invalid_data.tsv",  # File with non-integer values
        f"{SCRIPT_DIR}/data/na_filter_data.tsv",  # File with missing values
        f"{SCRIPT_DIR}/data/non_existent_file.tsv",
    ]


@pytest.fixture
def example_data():
    # Example data from challenge description
    data = pandas.read_table(
        f"{SCRIPT_DIR}/data/example_data.tsv", sep="\t", header=None, dtype=int, na_filter=False
    )
    return data


def test_load_data(file_paths):
    # Test loading valid data
    df = load_data(file_paths[0])
    assert isinstance(df, list)
    assert len(df) != 0

    # Test loading empty file
    with pytest.raises(typer.Exit):
        load_data(file_paths[1])

    # Test loading invalid data
    with pytest.raises(typer.Exit):
        load_data(file_paths[2])

    # Test loading file with missing values
    with pytest.raises(typer.Exit):
        load_data(file_paths[3])

    # Test loading non-existent file
    with pytest.raises(FileNotFoundError):
        load_data(file_paths[4])


def test_get_series_combinations(example_data):
    for _, row in example_data.iterrows():
        n = len(row)
        for r in range(1, n + 1):
            combinations_df = get_series_combinations(row, r)
            assert isinstance(combinations_df, pandas.DataFrame)
            assert len(combinations_df) == len(list(itertools.combinations(row.tolist(), r)))
            assert all(len(combo) == r for combo in combinations_df.values.tolist())
            if r == n:
                assert all(combinations_df.iloc[0,].values == row)
    # Test invalid r values
    with pytest.raises(ValueError):
        get_series_combinations(example_data.iloc[0], 0)
    with pytest.raises(ValueError):
        get_series_combinations(example_data.iloc[0], len(example_data.iloc[0]) + 1)


def test_get_diff(example_data):
    for _, row in example_data.iterrows():
        expected_row_diff = pandas.Series(dtype=int)
        expected_row_abs_diff = pandas.Series(dtype=int)
        for i in range(1, len(row)):
            expected_diff = row[i] - row[i - 1]
            expected_row_diff = pandas.concat(
                [expected_row_diff, pandas.Series([expected_diff])], ignore_index=True
            )
            expected_row_abs_diff = pandas.concat(
                [expected_row_abs_diff, pandas.Series([abs(expected_diff)])], ignore_index=True
            )
        pandas.testing.assert_series_equal(get_diff(row), expected_row_diff, check_names=False)
        pandas.testing.assert_series_equal(
            get_diff(row, absolute=True), expected_row_abs_diff, check_names=False
        )


def test_get_monotonicity_violation_count():
    test_cases = [
        (pandas.Series([1, 2, 3, 5]), 0),  # Strictly increasing
        (pandas.Series([3, 2, 1]), 0),  # Strictly decreasing
        (pandas.Series([1, 2, 2, 3, 4]), 0),  # Non-decreasing
        (pandas.Series([4, 3, 3, 2, 1]), 0),  # Non-increasing
        (pandas.Series([1, 3, 2, 4, 5]), 1),  # One violation
        (pandas.Series([1, 2, 3, 2, 1]), 2),  # Multiple violations
        (pandas.Series([1, 1, 1, 1]), 0),  # All elements equal
        (pandas.Series([1]), 0),  # Single element
        (pandas.Series([]), 0),  # Empty series
    ]
    for series, expected_count in test_cases:
        assert get_monotonicity_violation_count(series) == expected_count


def test_get_change_violation_count():
    test_cases = [
        (pandas.Series([1, 2, 3, 4, 5]), 0),  # All changes within [1, 3]
        (pandas.Series([1, 4, 7, 10]), 0),  # All changes within [1, 3]
        (pandas.Series([1, 5, 4, 13, 2]), 3),  # Mix of min and max change violations
        (pandas.Series([1, 12, 14, 60]), 2),  # Max change violations
        (pandas.Series([1, 1, 3, 3]), 2),  # Min change violations
        (pandas.Series([1]), 0),  # Single element
        (pandas.Series([]), 0),  # Empty series
    ]
    for series, expected_count in test_cases:
        assert get_change_violation_count(series, min_change=1, max_change=3) == expected_count
