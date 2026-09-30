# 11 — Comandos (backend)

Tudo roda **na raiz do projeto**. Há dois jeitos equivalentes: os atalhos do `Makefile` (precisa do `make` — instalação no [README](../README.md#instalando-o-make)) ou os comandos por extenso com o ambiente virtual ativado.

## 1. Ambiente virtual (`.venv`)

O ambiente virtual isola as libs do projeto das do sistema. Ele é criado uma vez; depois, **em cada terminal novo, ative-o** — a partir daí `python`, `pip`, `pytest`, `ruff` etc. passam a ser os do projeto.

**Criar** (uma vez, com Python 3.13):

| Sistema | Comando |
|---------|---------|
| Linux / macOS / WSL | `python3.13 -m venv .venv` |
| Windows (Git Bash, PowerShell ou cmd) | `py -3.13 -m venv .venv` (ou `python -m venv .venv`, se `python --version` já for 3.13) |

**Ativar** (em todo terminal novo):

| Terminal | Comando |
|----------|---------|
| Linux / macOS / WSL | `source .venv/bin/activate` |
| Windows — Git Bash | `source .venv/Scripts/activate` |
| Windows — PowerShell | `.venv\Scripts\Activate.ps1` |
| Windows — cmd | `.venv\Scripts\activate.bat` |

Ativado, o prompt mostra `(.venv)`. Para sair: `deactivate`.

> PowerShell bloqueando o script de ativação? Rode uma vez: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

**Instalar as dependências** (com o venv ativado):

```bash
pip install -r requirements-test.txt
```

## 2. Makefile — atalhos

`make help` lista os alvos. O Makefile usa o `.venv` sozinho (não precisa ativar) e detecta o Windows (`.venv/Scripts`).

| Alvo | O que faz |
|------|-----------|
| `make install` | Cria o `.venv` (se não existir) e instala `requirements-test.txt` |
| `make up` | `docker compose up --build` (imagem de runtime + DynamoDB Local) |
| `make down` | `docker compose down` |
| `make dev` | `docker compose -f docker-compose.dev.yml up --build` (reload) |
| `make run` | API fora do Docker com reload (banco em `localhost:8001`) |
| `make lint` | `ruff check` + `ruff format --check` + `lint-imports` |
| `make format` | `ruff format` + `ruff check --fix` |
| `make typecheck` | `mypy api tests` |
| `make test` | `coverage run -m pytest` + `coverage report` (mínimo 90%) |
| `make check` | `lint` + `typecheck` + `test` — validação completa antes de abrir o MR |
| `make openapi` | Atualiza o `openapi.json` versionado |
| `make build` | `docker build --target runtime -t bot-varejo-api:local .` |

`db-init` e `db-reset` entram no Makefile junto com `core/dynamodb` ([12](./12-persistencia-dynamodb.md#7-ambiente-local)), quando o primeiro context com tabela for implementado.

## 3. Comandos sem `make`

Com o venv ativado (§1), na raiz do projeto — iguais em qualquer sistema:

| Ação | Comando |
|------|---------|
| Rodar a API fora do Docker | `uvicorn api.app_run:create_app --factory --reload --port 8000` (banco: `APP_DYNAMODB_ENDPOINT_URL=http://localhost:8001` no `.env`) |
| Testes + cobertura | `coverage run -m pytest` e depois `coverage report` |
| Lint | `ruff check .` |
| Formatar | `ruff format .` |
| Tipos | `mypy api tests` |
| Fronteiras DDD | `lint-imports` |
| Exportar OpenAPI | `python -m api.scripts.export_openapi openapi.json` |

Docker e Docker Compose não dependem do venv: `docker compose up --build`, `docker compose -f docker-compose.dev.yml up --build`, `docker compose down`.
