# 🧹 Raw-to-Daily Splitter

[![codecov](https://codecov.io/gh/Djirlic/raw-to-daily-splitter/branch/main/graph/badge.svg)](https://codecov.io/gh/Djirlic/raw-to-daily-splitter)
![CI](https://github.com/Djirlic/raw-to-daily-splitter/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.13+-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen)


A Python CLI tool to split a raw CSV file (e.g. from [Kaggle Fraud Detection Dataset](https://www.kaggle.com/datasets/kartik2112/fraud-detection/data)) into **daily CSV files**, one per date found in the transaction data.

Built for professional-grade data engineering pipelines. Designed with testing and reproducibility in mind.

---

## 🚀 Features

- Reads large CSV files
- Cleans up unnecessary columns (`Unnamed: 0`)
- Converts and validates timestamp fields
- Groups transactions by date
- Saves each group as a daily CSV
- Logs warnings for malformed entries
- Fully tested & CI-validated

---

## 📦 Installation

Clone the repo and install dependencies using [Poetry](https://python-poetry.org):

```bash
poetry install --with dev,test
```

As an alternative to the poetry command, you can use:

```bash
make install
```

You’ll also need to have Python **3.13+** installed.

---

## ⚙️ Usage

```bash
poetry run python -m splitter.main --input ./data/raw/fraudTrain.csv --output ./data/processed/
```

Or simply:

```bash
make run
```

The `--input` and `--output` arguments are optional. Defaults are:

- `./data/raw/fraudTrain.csv`
- `./data/processed/`

---

## 🧪 Testing & Coverage

Run tests with:

```bash
make test
```

Generate coverage report:

```bash
make test-coverage
```

Check out the test files in `/tests` for detailed edge case handling.

---

## 🧼 Code Style

This project uses:

- [black](https://github.com/psf/black) for formatting
- [flake8](https://github.com/PyCQA/flake8) for linting
- [isort](https://github.com/PyCQA/isort) for import sorting
- [mypy](http://mypy-lang.org/) for type checks

These are automatically run via [pre-commit](https://pre-commit.com/). You can install it like this:

```bash
pre-commit install
```

Then your formatting/linting tools will run before each commit locally.

---

## 📁 Project Structure

```
raw-to-daily-splitter/
│
├── src/
│   └── splitter/            # Main logic (read, split, save)
│
├── tests/                   # Unit tests
├── data/                    # Expected location of raw/processed data
├── pyproject.toml           # Project + tool configuration
├── Makefile                 # Common tasks like test, run, format
├── .pre-commit-config.yaml  # Hooks for formatting/linting
```

---

## 💡 Future Ideas

- Make the date column configurable to support different kinds of datasets
- Add parallel processing to improve performance for large CSV files

---

Feel free to fork, contribute, or reach out if you found this useful 🙌
