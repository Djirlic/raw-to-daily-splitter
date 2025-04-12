import pandas as pd
import pytest

from splitter.splitter import split_by_day


def test_split_by_day_with_multiple_dates_creates_expected_files(tmp_path):
    test_data = pd.DataFrame(
        [
            ["2025-04-10 13:01:00", 1, "A"],
            ["2025-04-10 14:02:00", 2, "B"],
            ["2025-04-11 09:30:00", 3, "C"],
            ["2025-04-12 10:00:00", 4, "D"],
        ],
        columns=["trans_date_trans_time", "cc_num", "merchant"],
    )
    expected_files = {"2025-04-10.csv", "2025-04-11.csv", "2025-04-12.csv"}

    input_file = tmp_path / "test.csv"
    test_data.to_csv(input_file, index=False)

    output_dir = tmp_path / "processed"
    output_dir.mkdir()

    file_count = split_by_day(str(input_file), str(output_dir), "trans_date_trans_time")

    output_files = list(output_dir.iterdir())
    actual_files = {file.name for file in output_files}
    assert file_count == 3
    assert len(output_files) == 3
    assert all(file.suffix == ".csv" for file in output_files)
    assert actual_files == expected_files


def test_split_by_day_with_single_date_creates_expected_files(tmp_path):
    test_data = pd.DataFrame(
        [
            ["2025-04-10 13:01:00", 1, "A"],
            ["2025-04-10 14:02:00", 2, "B"],
            ["2025-04-10 09:30:00", 3, "C"],
            ["2025-04-10 10:00:00", 4, "D"],
        ],
        columns=["trans_date_trans_time", "cc_num", "merchant"],
    )
    expected_files = {"2025-04-10.csv"}

    input_file = tmp_path / "test.csv"
    test_data.to_csv(input_file, index=False)

    output_dir = tmp_path / "processed"
    output_dir.mkdir()

    file_count = split_by_day(str(input_file), str(output_dir), "trans_date_trans_time")

    output_files = list(output_dir.iterdir())
    actual_files = {file.name for file in output_files}
    assert file_count == 1
    assert len(output_files) == 1
    assert all(file.suffix == ".csv" for file in output_files)
    assert actual_files == expected_files


def test_split_by_day_with_empty_file_creates_no_files(tmp_path):
    test_data = pd.DataFrame(
        [],
        columns=["trans_date_trans_time", "cc_num", "merchant"],
    )

    input_file = tmp_path / "test.csv"
    test_data.to_csv(input_file, index=False)

    output_dir = tmp_path / "processed"
    output_dir.mkdir()

    file_count = split_by_day(str(input_file), str(output_dir), "trans_date_trans_time")

    output_files = list(output_dir.iterdir())
    assert file_count == 0
    assert len(output_files) == 0


def test_split_by_day_with_unnamed_leading_column_drops_leading_column(tmp_path):
    test_data = pd.DataFrame(
        {
            "trans_date_trans_time": [
                "2025-04-10 13:01:00",
                "2025-04-10 14:02:00",
                "2025-04-11 09:30:00",
                "2025-04-12 10:00:00",
            ],
            "cc_num": [1, 2, 3, 4],
            "merchant": ["A", "B", "C", "D"],
        }
    )

    # Save *with* index to simulate Unnamed: 0
    input_file = tmp_path / "test.csv"
    test_data.to_csv(input_file, index=True)

    output_dir = tmp_path / "processed"
    output_dir.mkdir()

    split_by_day(str(input_file), str(output_dir), "trans_date_trans_time")

    output_files = list(output_dir.iterdir())
    assert len(output_files) == 3

    for file in output_files:
        df = pd.read_csv(file)
        assert "Unnamed: 0" not in df.columns


def test_split_by_day_with_null_dates_drops_invalid_entries(tmp_path):
    test_data = pd.DataFrame(
        [
            ["2025-04-10 13:01:00", 1, "A"],
            [None, 2, "B"],
            ["2025-04-10 09:30:00", 3, "C"],
            ["2025-04-10 10:00:00", 4, "D"],
        ],
        columns=["trans_date_trans_time", "cc_num", "merchant"],
    )

    input_file = tmp_path / "test.csv"
    test_data.to_csv(input_file, index=False)

    output_dir = tmp_path / "processed"
    output_dir.mkdir()

    file_count = split_by_day(str(input_file), str(output_dir), "trans_date_trans_time")

    output_files = list(output_dir.iterdir())
    assert file_count == 1
    df = pd.read_csv(output_files[0])
    assert len(df) == 3
    assert not (df["cc_num"] == 2).any()


def test_split_by_day_with_malformed_dates_drops_invalid_entries(tmp_path):
    test_data = pd.DataFrame(
        [
            ["2025-04-10 13:01:00", 1, "A"],
            ["10.04.2025 12:00:00", 2, "B"],
            ["2025-04-10 09:30:00", 3, "C"],
            ["2025-04-10 10:00:00", 4, "D"],
        ],
        columns=["trans_date_trans_time", "cc_num", "merchant"],
    )

    input_file = tmp_path / "test.csv"
    test_data.to_csv(input_file, index=False)

    output_dir = tmp_path / "processed"
    output_dir.mkdir()

    file_count = split_by_day(str(input_file), str(output_dir), "trans_date_trans_time")

    output_files = list(output_dir.iterdir())
    assert file_count == 1
    df = pd.read_csv(output_files[0])
    assert len(df) == 3
    assert not (df["cc_num"] == 2).any()


def test_split_by_day_with_non_existing_input_path_throws_file_not_found_error(tmp_path):
    test_data = pd.DataFrame(
        [["2025-04-10 13:01:00", 1, "A"]],
        columns=["trans_date_trans_time", "cc_num", "merchant"],
    )

    input_file = tmp_path / "test.csv"
    invalid_input = tmp_path / "nonexistent.csv"
    test_data.to_csv(input_file, index=False)

    output_dir = tmp_path / "processed"
    output_dir.mkdir()

    with pytest.raises(FileNotFoundError):
        split_by_day(str(invalid_input), str(output_dir), "trans_date_trans_time")

    output_files = list(output_dir.iterdir())
    assert len(output_files) == 0


def test_split_by_day_with_output_dir_if_missing_creates_directory(tmp_path):
    test_data = pd.DataFrame(
        [["2025-04-10 13:01:00", 1, "A"]],
        columns=["trans_date_trans_time", "cc_num", "merchant"],
    )

    input_file = tmp_path / "test.csv"
    test_data.to_csv(input_file, index=False)

    output_dir = tmp_path / "new-output-dir"
    assert not output_dir.exists()

    file_count = split_by_day(str(input_file), str(output_dir), "trans_date_trans_time")

    assert file_count == 1
    assert output_dir.exists()
    output_files = list(output_dir.iterdir())
    assert len(output_files) == 1


def test_split_by_day_with_custom_date_field_creates_expected_files(tmp_path):
    test_data = pd.DataFrame(
        {
            "custom_date": [
                "2025-04-10 13:01:00",
                "2025-04-10 14:02:00",
                "2025-04-11 09:30:00",
            ],
            "cc_num": [1, 2, 3],
            "merchant": ["A", "B", "C"],
        }
    )
    expected_files = {"2025-04-10.csv", "2025-04-11.csv"}

    input_file = tmp_path / "test.csv"
    test_data.to_csv(input_file, index=False)

    output_dir = tmp_path / "processed"
    output_dir.mkdir()

    file_count = split_by_day(str(input_file), str(output_dir), "custom_date")

    output_files = list(output_dir.iterdir())
    actual_files = {file.name for file in output_files}
    assert file_count == 2
    assert len(output_files) == 2
    assert all(file.suffix == ".csv" for file in output_files)
    assert actual_files == expected_files
