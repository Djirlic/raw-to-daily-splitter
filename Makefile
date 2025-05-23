# Makefile at root of project

install:
	poetry install --with dev,test

test:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=src

run:
	poetry run python -m splitter.main

format:
	poetry run black .

lint:
	poetry run flake8 .

clean:
	find . -type d -name '__pycache__' -exec rm -r {} +

help:
	poetry run python -m splitter.main --help
