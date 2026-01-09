.PHONY: help setup venv install install-dev run lint format typecheck test docker-up docker-down docker-down-volumes db-up ci db-migrate-create db-migrate-run db-seed db-clean-hot db-reset

VENV_DIR=.venv
APP_DIR=src
DB_CONTAINER=postgres_local
DB_USER=USER
DB_NAME=SampleApi

help:
	@echo "Available targets:"
	@echo "  setup                Create venv and install dependencies"
	@echo "  venv                 Create virtual environment"
	@echo "  install              Install runtime dependencies"
	@echo "  install-dev          Install dev dependencies"
	@echo "  run                  Run the API with uvicorn"
	@echo "  lint                 Run ruff check (readonly)"
	@echo "  format               Run ruff fix (lint + imports) and format"
	@echo "  typecheck            Run mypy"
	@echo "  test                 Run pytest with coverage"
	@echo "  docker-up            Start full stack with docker-compose"
	@echo "  docker-down          Stop docker-compose stack"
	@echo "  docker-down-volumes  Stop stack and remove volumes"
	@echo "  db-up                Start only the database container"
	@echo "  ci                   Run lint, typecheck, and test"
	@echo "  db-migrate-create    Create a new migration (use NAME='...')"
	@echo "  db-migrate-run       Run all pending migrations"
	@echo "  db-seed              Seed the database with initial data"
	@echo "  db-clean-hot         Drop and recreate public schema"
	@echo "  db-reset             Wipe database and re-run migrations"

setup: venv install install-dev

venv:
	python3 -m venv $(VENV_DIR)

install:
	pip install -r requirements.txt
	$(MAKE) update-hooks

update-hooks:
	pre-commit install --hook-type pre-commit --hook-type commit-msg --hook-type pre-push

install-dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	$(MAKE) update-hooks

run:
	uvicorn main:app --reload --app-dir $(APP_DIR)

lint:
	ruff check .
	ruff format --check .

format:
	ruff check --fix .
	ruff format .

typecheck:
	mypy .

test:
	.venv/bin/pytest

docker-up:
	docker-compose up --build -d

docker-down:
	docker-compose down

docker-down-volumes:
	docker compose down -v

db-up:
	docker-compose up -d db

ci: lint typecheck test

db-migrate-create:
	alembic revision --autogenerate -m "$(NAME)"

db-migrate-run:
	alembic upgrade head


db-seed:
	PYTHONPATH=src python seed.py all

db-clean-hot:
	docker exec $(DB_CONTAINER) psql -U $(DB_USER) -d $(DB_NAME) -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

db-reset:db-clean-hot db-migrate-run
