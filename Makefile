.PHONY: tests lint format migrate collectstatic createsuperuser db_and_redis load_test_data setup_periodic_tasks draw_winner quick_start coverage

quick_start:
	@if [ ! -f .env.docker ]; then \
		echo "Creating .env.docker from .env.docker.example..."; \
		cp .env.docker.example .env.docker; \
	fi
	docker compose --env-file .env.docker up --build -d
	$(MAKE) migrate
	$(MAKE) setup_periodic_tasks
	$(MAKE) load_test_data
	@echo ""
	@echo "Service is ready!"
	@echo "  http://localhost:8000"
	@echo "  Admin: http://localhost:8000/admin/ (admin / admin)"
	@echo "  Participants: alice, bob, charlie (password: password123)"

tests:
	$(MAKE) db_and_redis
	poetry install --no-root --no-interaction
	poetry run pytest -v

coverage:
	poetry install --no-root --no-interaction
	poetry run pytest --cov=apps --cov-report=term-missing --cov-fail-under=95 -v

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

draw_winner:
	docker compose --env-file .env.docker exec lottery_service python manage.py draw_winner

setup_periodic_tasks:
	docker compose --env-file .env.docker exec lottery_service python manage.py setup_periodic_tasks

db_and_redis:
	docker compose up -d db redis
