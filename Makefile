# Makefile at root of project

install:
	poetry install --with test

test:
	poetry run pytest

run:
	poetry run python src/splitter/main.py

format:
	poetry run black .

lint:
	poetry run flake8 .

clean:
	find . -type d -name '__pycache__' -exec rm -r {} +
