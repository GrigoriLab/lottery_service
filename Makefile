.PHONY: tests lint format migrate collectstatic

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

migrate:
	poetry run python manage.py migrate --no-input

collectstatic:
	poetry run python manage.py collectstatic --no-input
