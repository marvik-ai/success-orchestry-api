.PHONY: install lint format typecheck test ci

# This is now the ONLY command a dev needs to run to set up
install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pre-commit install --hook-type pre-commit --hook-type commit-msg --hook-type pre-push

lint:
	ruff check .
	ruff format --check .

format:
	ruff check --fix .
	ruff format .

typecheck:
	mypy .

test:
	pytest --cov=app --cov-report=term-missing

# Unified command for CI and local verification
ci: lint typecheck test