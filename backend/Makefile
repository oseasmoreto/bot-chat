# Atalhos do dia a dia. Comandos equivalentes sem make: README.md e docs/11-ci.md.
PYTHON ?= python3.13
VENV   := .venv
BIN    := $(VENV)/bin
export PYTHONPATH := .

.DEFAULT_GOAL := help
.PHONY: help setup install up down dev run test lint format typecheck check openapi build

help: ## Lista os alvos
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  %-10s %s\n", $$1, $$2}'

$(BIN)/python:
	$(PYTHON) -m venv $(VENV)

install: $(BIN)/python ## Instala as dependências (runtime + testes e qualidade) no .venv
	$(BIN)/pip install -r requirements-test.txt

setup: install ## Prepara o clone: dependências, hooks e template de commit
	$(BIN)/pre-commit install
	git config commit.template .gitmessage

up: ## Sobe a imagem de runtime + DynamoDB Local
	docker compose up --build

down: ## Para os containers
	docker compose down

dev: ## Sobe a API com reload + DynamoDB Local
	docker compose -f docker-compose.dev.yml up --build

run: ## Roda a API fora do Docker (banco em localhost:8001)
	APP_DYNAMODB_ENDPOINT_URL=$${APP_DYNAMODB_ENDPOINT_URL:-http://localhost:8001} \
		$(BIN)/uvicorn api.app_run:create_app --factory --reload --port 8000

test: ## Testes com cobertura (mínimo 90%)
	$(BIN)/coverage run -m pytest
	$(BIN)/coverage report

lint: ## ruff (lint e formatação) + fronteiras DDD
	$(BIN)/ruff check .
	$(BIN)/ruff format --check .
	$(BIN)/lint-imports

format: ## Formata e aplica correções automáticas
	$(BIN)/ruff format .
	$(BIN)/ruff check --fix .

typecheck: ## mypy --strict
	$(BIN)/mypy api tests

check: lint typecheck test ## Tudo o que o CI valida

openapi: ## Atualiza o openapi.json versionado
	$(BIN)/python -m api.scripts.export_openapi openapi.json

build: ## Gera a imagem de runtime
	docker build --target runtime -t bot-varejo-api:local .
