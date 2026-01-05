.PHONY: help setup venv install install-dev run lint format typecheck test docker-up docker-down db-up

VENV_DIR=venv
APP_DIR=src
VENV_BIN=$(VENV_DIR)/bin
PYTHON=$(VENV_BIN)/python
PIP=$(VENV_BIN)/pip
UVICORN=$(VENV_BIN)/uvicorn
RUFF=$(VENV_BIN)/ruff
BLACK=$(VENV_BIN)/black
MYPY=$(VENV_BIN)/mypy
PYTEST=$(VENV_BIN)/pytest

help:
	@echo "Available targets:"
	@echo "  setup        Create venv and install dependencies"
	@echo "  venv         Create virtual environment"
	@echo "  install      Install runtime dependencies"
	@echo "  install-dev  Install dev dependencies"
	@echo "  run          Run the API with uvicorn"
	@echo "  lint         Run ruff"
	@echo "  format       Run black"
	@echo "  typecheck    Run mypy"
	@echo "  test         Run pytest"
	@echo "  docker-up    Start full stack with docker-compose"
	@echo "  docker-down  Stop docker-compose stack"
	@echo "  db-up        Start only the database container"

setup: venv install install-dev

venv:
	python3 -m venv $(VENV_DIR)

install:
	$(PIP) install -r requirements.txt

install-dev:
	$(PIP) install -r requirements-dev.txt

run:
	$(UVICORN) main:app --reload --app-dir $(APP_DIR)

lint:
	$(RUFF) check $(APP_DIR) tests

format:
	$(BLACK) $(APP_DIR) tests

typecheck:
	PYTHONPATH=$(APP_DIR) $(MYPY) $(APP_DIR)

test:
	PYTHONPATH=$(APP_DIR) $(PYTEST)

docker-up:
	docker-compose up --build

docker-down:
	docker-compose down

db-up:
	docker-compose up -d db
