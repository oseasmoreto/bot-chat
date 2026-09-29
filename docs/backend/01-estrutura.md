# Backend — Estrutura de pastas

> Localização no repositório: `backend/`. Visão do monorepo completo em [02 — Estrutura do repositório](../02-estrutura-repositorio.md).

```text
backend/
├── pyproject.toml               # dependências, config de ruff, mypy, pytest, coverage
├── uv.lock
├── README.md                    # comandos específicos do backend
├── src/
│   └── bot_varejo/
│       ├── __init__.py
│       ├── main.py              # create_app(): composição, routers, middlewares
│       ├── container.py         # composition root: instancia adapters/casos de uso + get_container
│       ├── core/                # "shared kernel" — transversal a todos os contexts
│       │   ├── __init__.py
│       │   ├── config.py        # Settings (pydantic-settings) — lê variáveis de ambiente
│       │   ├── logging.py       # configuração de log estruturado (JSON)
│       │   ├── errors.py        # exceções base + handlers HTTP padronizados
│       │   ├── scope.py         # enum Scope (PUBLIC, ADMIN)
│       │   ├── schemas.py       # BaseSchema (Pydantic com camelCase)
│       │   └── websocket/
│       │       ├── __init__.py
│       │       ├── messages.py  # envelope WsMessage (type, id, payload)
│       │       └── dispatcher.py# MessageDispatcher: registra handlers por "type"
│       ├── api/                 # composição por escopo (agrega routers dos contexts)
│       │   ├── __init__.py
│       │   ├── public.py        # APIRouter prefix=/api/v1/public
│       │   ├── admin.py         # APIRouter prefix=/api/v1/admin
│       │   └── websocket.py     # rotas /ws/public e /ws/admin
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
│           └── export_openapi.py          # gera openapi.json para o api-client
└── tests/
    ├── __init__.py
    ├── conftest.py              # fixtures: app, client async, ws client
    ├── fakes.py                 # dublês das ports: FakeClock, StubCheck
    ├── unit/
    │   └── contexts/health/
    │       ├── domain/test_entities.py
    │       └── application/test_get_health.py
    ├── integration/
    │   ├── api/test_public_health.py
    │   ├── api/test_admin_health.py
    │   └── websocket/test_health_ws.py
    └── contract/
        └── test_openapi_schema.py   # garante que o openapi.json commitado está atualizado
```

> **Padrão `src/`**: o código fica em `src/bot_varejo/` para impedir import acidental sem instalação e garantir que os testes rodem contra o pacote instalado.
