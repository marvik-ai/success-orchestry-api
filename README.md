# Setup and Run
## 1. Prerequisites
  Docker Desktop installed.
  Python 3.14.2 installed locally.
  A DB client like DBeaver (optional).

## 2. Option A: Local Development (Recommended)
  Ideal for live code changes with hot-reload.
  ### Step 1: Start the database in Docker
    docker-compose up -d db
  ### Step 2: Set up the virtual environment
  #### Create the environment
      python -m venv venv
  #### Activate on macOS/Linux:
      source venv/bin/activate
  #### Activate on Windows:
      .\venv\Scripts\activate
  ### Step 3: Install dependencies
    pip install -r requirements.txt
  ### Step 4: Run the application
    uvicorn app.main:app --reload

Access: http://localhost:8000

## 3. Option B: Full Docker Run
  To bring up the full stack (API + database) in isolation:
  docker-compose up --build

## 4. Code Quality
  ### Development dependencies (Python)
    pip install -r requirements-dev.txt
  ### Linting and formatting (Python)
    ruff check .
    black .
    mypy app
  ### Frontend tooling (Husky, ESLint, Prettier)
    npm install
    npm run lint
    npm run format
