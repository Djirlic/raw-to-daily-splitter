import datetime
import os
from collections.abc import Iterable

import pandas as pd

from splitter.logger import logger


def split_by_day(input_path: str, output_dir: str) -> int:
    """
    Splits the data by day.

    This function reads the raw CSV file, splits the data by day,
    and saves the split data to a new CSV files (one for each date).

    Args:
        input_path (str): Path to the raw CSV file.
        output_dir (str): Directory to save the split CSV files.
    """
    df = read_raw_csv(path=input_path)
    grouped_by_date = df.groupby(df["trans_date_trans_time"].dt.date)
    save_grouped_data_to_csvs(grouped_by_date, output_dir)
    return len(grouped_by_date)


def read_raw_csv(path: str) -> pd.DataFrame:
    """
    Reads a CSV file and returns a DataFrame.

    Args:
        path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: DataFrame containing the data from the CSV file.
    """
    df = pd.read_csv(path)
    df["trans_date_trans_time"] = pd.to_datetime(df["trans_date_trans_time"], errors="coerce")

    if df["trans_date_trans_time"].isnull().any():
        bad_rows = df[df["trans_date_trans_time"].isnull()]
        logger.warning(f"⚠️ Warning: {len(bad_rows)} rows had invalid date format.")

    if "Unnamed: 0" in df.columns:
        logger.info("🧹 Dropping 'Unnamed: 0' (non-domain index)")
        df = df.drop(columns=["Unnamed: 0"])

    if df.empty:
        logger.warning(f"⚠️ The input file {path} is empty — skipping processing.")

    return df


def save_grouped_data_to_csvs(
    grouped_data: Iterable[tuple[datetime.date, pd.DataFrame]], output_dir: str
) -> None:
    """
    Saves grouped data to CSV files.

    Args:
        grouped_data (Iterable[tuple[datetime.date, pd.DataFrame]]):
          A tuple containing the date and the grouped data for this date.
        output_dir (str): Directory to save the CSV files.
    """
    os.makedirs(output_dir, exist_ok=True)
    for date, group in grouped_data:
        date_str = date.strftime("%Y-%m-%d")
        output_path = os.path.join(output_dir, f"{date_str}.csv")
        group.to_csv(output_path, index=False)
        logger.info(f"Saved {len(group)} rows to {output_path}")
