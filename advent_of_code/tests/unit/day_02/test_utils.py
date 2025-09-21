from advent_of_code.day_02.utils import load_data, get_diff
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
