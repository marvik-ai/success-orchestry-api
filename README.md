# Success Orchestry API

## Introduction
Success Orchestry API is a FastAPI service template designed to be simple to start and easy to scale. It follows a clear separation of concerns so new features can be added without mixing responsibilities.
Current implemented domains: Health and Employee.

## Architecture Overview
- Controllers: Define HTTP routes, request/response handling, and dependency wiring.
- Services: Contain business logic and orchestrate use cases.
- Repositories: Handle database access and persistence.
- Models: Define domain and API data structures.
- Common: Shared configuration, logging, and database setup.
Project code lives under `src/`.

## Setup and Run
## 1. Prerequisites
  Docker Desktop installed.
  Python 3.14.2 installed locally.
  A DB client like DBeaver (optional).
  Copy `.env.example` to `.env` and update values as needed.

## 2. Option A: Local Development (Recommended)
  Ideal for live code changes with hot-reload.
  ### Step 1: Start the database in Docker
    docker-compose up -d db
    # or: make db-up
  ### Step 2: Set up the virtual environment
  #### Create the environment
      python -m venv venv
  #### Activate on macOS/Linux:
      source venv/bin/activate
  #### Activate on Windows:
      .\venv\Scripts\activate
  ### Step 3: Install dependencies
    pip install -r requirements.txt
  ### Step 4: Run the migrations
    alembic upgrade head
    # or: make db-migrate-run
  ### Step 5: Run the application
    uvicorn main:app --reload --app-dir src
    # or: make run (uses venv/bin/uvicorn)

  ### Alternative: Use Makefile for local API + Docker DB
    make db-up
    make db-migrate-run
    make run

  Access: http://localhost:8000

## 3. Option B: Full Docker Run
  To bring up the full stack (API + database) in isolation:
  1. docker-compose up --build
    # or: make docker-up
  2. make db-migrate-run

  ### Alternative: Use Makefile for full Docker
    make docker-up
    make db-migrate-run

## 4. Code Quality
  ### Development dependencies (Python)
    pip install -r requirements-dev.txt
    # or: make install-dev (uses venv/bin/pip)
  ### Linting and formatting (Python)
    ruff check .
    black .
    mypy app
    # or: make lint, make format, make typecheck

## 5. Tests
  ### Run tests
    pytest
    # or: make test

## 6. Migrations
  * **db-migrate-create name={Name}** generates a new migration with the name {Name}
  * **db-migrate-run** applies all pending migrations to update the database to the latest version (head).
  * **db-reset** wipes all data and tables (drops schema) and re-applies all migrations from scratch.

## 7. Fake Data generation
   * **db-seed** populates the database with initial/dummy data.

## 8. Update hooks
  make update-hooks
