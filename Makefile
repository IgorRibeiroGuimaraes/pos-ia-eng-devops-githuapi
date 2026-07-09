.PHONY: up down logs build shell migrate revision extract run-pipeline test lint format install clean

## ── Containers ────────────────────────────────────────────────────────────────
up:
	podman-compose -f compose.yaml up -d

down:
	podman-compose -f compose.yaml down

logs:
	podman-compose -f compose.yaml logs -f

build:
	podman-compose -f compose.yaml build

shell:
	podman-compose -f compose.yaml exec api bash

## ── Banco de Dados / Alembic ──────────────────────────────────────────────────
migrate:
	alembic upgrade head

revision:
	alembic revision --autogenerate -m "$(msg)"

downgrade:
	alembic downgrade -1

## ── Pipeline ──────────────────────────────────────────────────────────────────
extract:
	python -c "from src.database.session import SessionLocal; from src.services.pipeline_service import run_pipeline; db = SessionLocal(); run_pipeline(db)"

run-pipeline: extract

## ── Prefect ───────────────────────────────────────────────────────────────────
prefect:
	prefect server start

## ── Testes ────────────────────────────────────────────────────────────────────
test:
	pytest

test-cov:
	pytest --cov=src --cov-report=html

## ── Qualidade de Código ───────────────────────────────────────────────────────
lint:
	ruff check src tests

format:
	black src tests
	ruff check --fix src tests

## ── Instalação ────────────────────────────────────────────────────────────────
install:
	pip install -e ".[dev]"

install-prod:
	pip install -e .

## ── Limpeza ───────────────────────────────────────────────────────────────────
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf .pytest_cache htmlcov .coverage
