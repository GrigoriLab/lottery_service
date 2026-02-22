.PHONY: tests lint format

tests:
	poetry install --no-root --no-interaction
	poetry run pytest -v

lint:
	poetry install --no-root --no-interaction
	poetry run ruff check .

format:
	poetry install --no-root --no-interaction
	poetry run ruff check --fix .
	poetry run ruff format .
