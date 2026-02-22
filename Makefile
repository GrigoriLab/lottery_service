.PHONY: tests

tests:
	poetry install --no-root --no-interaction
	poetry run pytest -v
