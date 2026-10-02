# Atalhos do dia a dia. Comandos equivalentes sem make: docs/11-comandos.md.
# Funciona no Linux, macOS, WSL e no Git Bash do Windows.
VENV := .venv
ifeq ($(OS),Windows_NT)
PYTHON ?= python
BIN    := $(VENV)/Scripts
else
PYTHON ?= python3.13
BIN    := $(VENV)/bin
endif

.DEFAULT_GOAL := help
.PHONY: help install up down dev run test lint format typecheck check openapi build

help: ## Lista os alvos
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  %-10s %s\n", $$1, $$2}'

$(VENV)/pyvenv.cfg:
	$(PYTHON) -m venv $(VENV)

install: $(VENV)/pyvenv.cfg ## Cria o .venv e instala as dependências (runtime + testes e qualidade)
	$(BIN)/python -m pip install -r requirements-test.txt

up: ## Sobe a imagem de runtime + DynamoDB Local
	docker compose up --build

down: ## Para os containers
	docker compose down

dev: ## Sobe a API com reload + DynamoDB Local
	docker compose -f docker-compose.dev.yml up --build

run: ## Roda a API fora do Docker (banco em localhost:8001)
	APP_DYNAMODB_ENDPOINT_URL=$${APP_DYNAMODB_ENDPOINT_URL:-http://localhost:8001} \
		$(BIN)/uvicorn main:app --reload --reload-dir api --port 8000

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
	$(BIN)/mypy main.py api tests

check: lint typecheck test ## Validação completa: lint, tipos e testes

openapi: ## Atualiza o openapi.json versionado
	$(BIN)/python -m api.scripts.export_openapi openapi.json

build: ## Gera a imagem de runtime
	docker build --target runtime -t bot-varejo-api:local .
