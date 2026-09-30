# 02 — Estrutura de pastas (backend)

O backend é um **projeto independente**: tem seu próprio README, docs, Dockerfile, docker compose, Makefile e pipeline. Nada aqui depende do código do frontend — a única ligação é o contrato HTTP/WS ([06](./06-contratos-api.md)).

```text
backend/
├── README.md                    # passo a passo para rodar localmente
├── CONTRIBUTING.md              # branches, commits, MRs, versionamento, validações
├── .gitmessage                  # template de mensagem de commit
├── docs/                        # esta documentação (+ adr/, tasks/)
├── pyproject.toml               # dependências e config de ruff, mypy, pytest, coverage, import-linter
├── uv.lock
├── .python-version              # 3.13
├── openapi.json                 # contrato exportado (make openapi) — versionado, validado no CI
├── Dockerfile                   # multi-stage: dev, builder, runtime (python:3.13-slim)
├── docker-compose.yml           # bot-varejo-api (runtime) + bot-varejo-dynamodb
├── docker-compose.dev.yml       # bot-varejo-api (--reload) + bot-varejo-dynamodb
├── Makefile                     # make setup, up, dev, test, lint, openapi…
├── .env.example                 # todas as variáveis documentadas
├── .dockerignore
├── .gitignore                   # arquivos fora do git (.venv, caches, .env…)
├── .gitlab-ci.yml               # pipeline: validate, lint, testes, build, publish
├── .gitlab/
│   └── merge_request_templates/ # templates de MR do backend: Default, Bugfix, Hotfix, Docs
├── src/
│   └── bot_varejo/
│       ├── __init__.py
│       ├── main.py              # create_app(): composição, CORS, routers, handlers de erro
│       ├── container.py         # composition root: instancia adapters/casos de uso + get_container
│       ├── core/                # "shared kernel" — transversal a todos os contexts
│       │   ├── __init__.py
│       │   ├── config.py        # Settings (pydantic-settings) — variáveis APP_*
│       │   ├── logging.py       # log estruturado (JSON)
│       │   ├── errors.py        # exceções base + handlers HTTP padronizados
│       │   ├── request_id.py    # middleware X-Request-ID
│       │   ├── scope.py         # enum Scope (PUBLIC, ADMIN)
│       │   ├── schemas.py       # BaseSchema (Pydantic com camelCase)
│       │   └── websocket/
│       │       ├── __init__.py
│       │       ├── messages.py  # envelope WsMessage (type, id, payload)
│       │       └── dispatcher.py# MessageDispatcher: registra handlers por "type"
│       │   └── dynamodb/        # acesso ao DynamoDB (ver docs/12): resource, tables, codecs, paginação, health
│       ├── api/                 # composição por escopo (agrega routers dos contexts)
│       │   ├── __init__.py
│       │   ├── public.py        # APIRouter prefix=/api/v1/public
│       │   ├── admin.py         # APIRouter prefix=/api/v1/admin
│       │   └── websocket.py     # /api/v1/ws/public e /api/v1/ws/admin (+ validação de Origin)
│       ├── contexts/            # bounded contexts (DDD)
│       │   ├── __init__.py
│       │   └── health/
│       │       ├── __init__.py
│       │       ├── domain/
│       │       │   ├── __init__.py
│       │       │   ├── entities.py        # HealthReport, ComponentHealth
│       │       │   ├── value_objects.py   # HealthStatus
│       │       │   └── ports.py           # ClockPort, HealthCheckPort (Protocols)
│       │       ├── application/
│       │       │   ├── __init__.py
│       │       │   └── get_health.py      # GetHealthUseCase
│       │       ├── infrastructure/
│       │       │   ├── __init__.py
│       │       │   └── system_clock.py    # SystemClock (implementa ClockPort)
│       │       └── presentation/
│       │           ├── __init__.py
│       │           ├── schemas.py         # HealthResponse (Pydantic)
│       │           ├── dependencies.py    # providers para Depends()
│       │           ├── http.py            # build_health_router(scope)
│       │           └── ws_handlers.py     # handler de "health.ping"
│       └── scripts/
│           ├── export_openapi.py          # gera openapi.json (make openapi)
│           └── create_tables.py           # cria as tabelas no DynamoDB Local (make db-init)
└── tests/
    ├── __init__.py
    ├── conftest.py              # fixtures: app, client async, ws client, ALLOWED_ORIGIN
    ├── fakes.py                 # dublês das ports: FakeClock, StubCheck
    ├── unit/
    │   └── contexts/health/
    │       ├── domain/test_entities.py
    │       └── application/test_get_health.py
    ├── integration/
    │   ├── api/test_public_health.py
    │   ├── api/test_admin_health.py
    │   ├── api/test_cors.py
    │   └── websocket/test_health_ws.py
    └── contract/
        └── test_openapi_schema.py   # openapi.json versionado = gerado
```

> **Padrão `src/`**: o código fica em `src/bot_varejo/` para impedir import acidental sem instalação e garantir que os testes rodem contra o pacote instalado.

## Arquivos gerados

| Arquivo | Gerado por | Versionado? |
|---------|-----------|-------------|
| `openapi.json` | `make openapi` | ✅ (o diff mostra mudanças de contrato no MR) |
| `.venv/` | `uv sync` | ❌ |
| `.coverage`, `htmlcov/` | pytest-cov | ❌ |
