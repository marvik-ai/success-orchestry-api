.PHONY: help setup venv install install-dev run lint format typecheck test docker-up docker-down db-up ci

VENV_DIR=.venv
APP_DIR=src

help:
	@echo "Available targets:"
	@echo "  setup        Create venv and install dependencies"
	@echo "  venv         Create virtual environment"
	@echo "  install      Install runtime dependencies"
	@echo "  install-dev  Install dev dependencies"
	@echo "  run          Run the API with uvicorn"
	@echo "  lint         Run ruff check (readonly)"
	@echo "  format       Run ruff fix (lint + imports) and format"
	@echo "  typecheck    Run mypy"
	@echo "  test         Run pytest with coverage"
	@echo "  docker-up    Start full stack with docker-compose"
	@echo "  docker-down  Stop docker-compose stack"
	@echo "  db-up        Start only the database container"

setup: venv install install-dev

venv:
	python3 -m venv $(VENV_DIR)

install:
	pip install -r requirements.txt
	pre-commit install --hook-type pre-commit --hook-type commit-msg --hook-type pre-push

install-dev:
	pip install -r requirements-dev.txt

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
	docker-compose up --build

docker-down:
	docker-compose down

db-up:
	docker-compose up -d db

ci: lint typecheck test

db-migrate:
	alembic revision --autogenerate -m $(name)

db-upgrade:
	alembic upgrade head

db-generate:
	python seed.py all
