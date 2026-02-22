.PHONY: tests lint format migrate collectstatic createsuperuser db_and_redis load_test_data setup_periodic_tasks

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
	docker compose --env-file .env.docker exec lottery_service python manage.py migrate

createsuperuser:
	docker compose --env-file .env.docker exec lottery_service python manage.py createsuperuser

load_test_data:
	docker compose --env-file .env.docker exec lottery_service python manage.py create_test_data

setup_periodic_tasks:
	docker compose --env-file .env.docker exec lottery_service python manage.py setup_periodic_tasks

db_and_redis:
	docker compose up -d db redis
