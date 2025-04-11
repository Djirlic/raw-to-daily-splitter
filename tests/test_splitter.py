import pandas as pd

from splitter.splitter import split_by_day


def test_split_by_day_creates_expected_files(tmp_path):
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

    file_count = split_by_day(str(input_file), str(output_dir))

    output_files = list(output_dir.iterdir())
    actual_files = {file.name for file in output_files}
    assert file_count == 3
    assert len(output_files) == 3
    assert all(file.suffix == ".csv" for file in output_files)
    assert actual_files == expected_files
