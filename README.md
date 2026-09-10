# Object-Oriented Python Analytics Application

A small production-style analytics service that combines a REST API, relational persistence, validation, testing, containerization, and the original stakeholder-reporting workflow.

## Why this project exists
The application turns program-participation records into validated, queryable data and stakeholder analytics. It is intentionally structured as a software-engineering project rather than a notebook-only analysis: API routes, schemas, database models, service logic, tests, Docker packaging, and reporting are separated into clear components.

## Technology
- Python 3.11+
- FastAPI + Pydantic
- SQLAlchemy ORM
- PostgreSQL in Docker Compose; SQLite is used by isolated tests
- Pytest + FastAPI TestClient
- Docker / Docker Compose
- Pandas, Matplotlib and OpenPyXL for the reporting workflow

## Application structure
- `src/main.py` - REST API endpoints and dependency wiring
- `src/database.py` - SQLAlchemy engine/session configuration
- `src/models.py` - relational program-record model
- `src/schemas.py` - validated request/response schemas
- `src/service.py` - create, query and SQL aggregation logic
- `src/build_dashboard.py` - original analytics/dashboard workflow
- `tests/test_api.py` - API, validation, duplicate-key and aggregation tests
- `tests/test_dashboard.py` - reporting validation tests
- `data/sample_program_data.csv` - documented synthetic sample; no confidential participant data is published
- `Dockerfile` and `docker-compose.yml` - containerized API + PostgreSQL stack

## REST endpoints
- `GET /health` - service health
- `POST /programs` - add a validated program record
- `GET /programs?department=Computing` - query stored records with an optional department filter
- `GET /analytics/departments` - SQL-backed department summary with program count, funding, volunteers and average satisfaction

Duplicate `program_id` values are rejected with HTTP 409. Pydantic validation rejects invalid values such as satisfaction outside the supported 1-5 range before persistence.

## Run with Docker
```bash
docker compose up --build
```
Then open `http://localhost:8000/docs` for the interactive OpenAPI interface.

## Run locally
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn src.main:app --reload
```
The local default database is SQLite (`programs.db`). Set `DATABASE_URL` to use another SQLAlchemy-compatible database.

## Run tests
```bash
pytest -q
```
The API test suite uses an isolated in-memory SQLite database and covers health checks, record creation/filtering, duplicate-ID handling, request validation and SQL aggregation.

## Reporting workflow
The original reporting component remains available:
```bash
python src/build_dashboard.py --input data/sample_program_data.csv
```
It validates the sample records and generates stakeholder-ready summary outputs from the documented synthetic dataset.

## Resume-relevant engineering evidence
This repository demonstrates Python/OOP application structure, REST API design, RDBMS/ORM usage, validation and error handling, automated testing, SQL aggregation, Docker containerization, data-quality checks, and technical documentation in one reproducible project.
