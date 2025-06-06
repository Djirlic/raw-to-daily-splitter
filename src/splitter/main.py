import argparse

from splitter.logger import logger
from splitter.splitter import split_by_day

DEFAULT_RAW_DATA_PATH = "./data/raw/fraudTrain.csv"
DEFAULT_OUTPUT_DIR = "./data/processed/"
DEFAULT_DATE_FIELD = "trans_date_trans_time"


def main():
    """
    Main function to execute the data splitting process.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default=DEFAULT_RAW_DATA_PATH,
        help=f"Path to raw CSV file (default {DEFAULT_RAW_DATA_PATH})",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT_DIR,
        help=f"Folder to write split CSV files (default {DEFAULT_OUTPUT_DIR})",
    )
    parser.add_argument(
        "--date-field",
        default=DEFAULT_DATE_FIELD,
        help=(
            "Name of the column that includes the dates to split the CSV by "
            f"(default {DEFAULT_DATE_FIELD})"
        ),
    )
    args = parser.parse_args()

    created_files = split_by_day(args.input, args.output, args.date_field)
    logger.info(f"✅ Successfully split data into {created_files} files.")
    logger.info("✅ Finished splitting data by day.")


if __name__ == "__main__":
    main()
