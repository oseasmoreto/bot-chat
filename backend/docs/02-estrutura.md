# 02 — Estrutura de pastas (backend)

O backend é um **projeto independente**: tem seu próprio README, docs, Dockerfile, docker compose e Makefile. Nada aqui depende do código do frontend — a única ligação é o contrato HTTP/WS ([06](./06-contratos-api.md)).

```text
backend/
├── README.md                    # passo a passo para rodar localmente
├── CONTRIBUTING.md              # branches, commits, MRs, versionamento, validações
├── docs/                        # esta documentação (+ adr/, tasks/)
├── config/                      # arquivos de deploy/infra da plataforma — não alterar a estrutura
├── certificates/                # certificados de CA adicionais (.crt)
├── requirements.txt             # dependências de runtime, versões fixadas (docs/13)
├── requirements-test.txt        # -r requirements.txt + testes e qualidade (docs/13)
├── pyproject.toml               # config de ruff, mypy, pytest, coverage, import-linter (sem dependências)
├── openapi.json                 # contrato exportado (make openapi) — versionado, validado pelo teste de contrato
├── Dockerfile                   # multi-stage: dev, builder, runtime (python:3.13-slim)
├── docker-compose.yml           # bot-varejo-api (runtime) + bot-varejo-dynamodb
├── docker-compose.dev.yml       # bot-varejo-api (--reload) + bot-varejo-dynamodb
├── Makefile                     # make install, up, dev, test, check, openapi…
├── .env.example                 # todas as variáveis documentadas
├── .dockerignore
├── .gitignore                   # arquivos fora do git (.venv, caches, .env…)
├── .gitlab/
│   └── merge_request_templates/ # templates de MR do backend: Default, Bugfix, Docs, Hotfix, Release
├── .github/                     # GitHub Copilot (docs/14): instruções, prompts e agente
│   ├── copilot-instructions.md  # regras gerais do projeto
│   ├── instructions/            # regras por camada/pasta (*.instructions.md, applyTo)
│   ├── prompts/                 # /novo-context, /novo-modulo, /novo-endpoint, /nova-mensagem-ws, /revisar-arquitetura
│   └── agents/                  # backend-ddd.agent.md — agente especialista
├── api/                         # código da aplicação (pacote Python `api`)
│   ├── __init__.py
│   ├── app_run.py               # create_app(): composição, middlewares, routers, handlers de erro
│   ├── config.py                # Settings (pydantic-settings) — variáveis APP_*
│   ├── container.py             # composition root: instancia adapters/casos de uso + get_container
│   ├── core/                    # "shared kernel" — transversal a todos os contexts
│   │   ├── __init__.py
│   │   ├── cors.py              # configure_cors(): origens de APP_CORS_ORIGINS
│   │   ├── swagger.py           # URLs de /api/docs, /api/redoc, /api/openapi.json (APP_DOCS_ENABLED)
│   │   ├── logs.py              # log estruturado (JSON) no stdout
│   │   ├── exceptions.py        # DomainError, NotFoundError, ConflictError (Python puro, usado pelo domínio)
│   │   ├── errors.py            # handlers: exceção → resposta de erro padronizada
│   │   ├── request_id.py        # middleware X-Request-ID
│   │   ├── scope.py             # enum Scope (PUBLIC, ADMIN)
│   │   ├── schemas.py           # BaseSchema (Pydantic com camelCase)
│   │   ├── websocket/
│   │   │   ├── __init__.py
│   │   │   ├── messages.py      # envelope WsMessage (type, id, payload)
│   │   │   └── dispatcher.py    # MessageDispatcher: registra handlers por "type"
│   │   └── dynamodb/            # acesso ao DynamoDB (docs/12) — criado com o primeiro context persistido
│   ├── routes/                  # composição por escopo (agrega routers dos contexts)
│   │   ├── __init__.py
│   │   ├── public.py            # APIRouter prefix=/api/v1/public
│   │   ├── admin.py             # APIRouter prefix=/api/v1/admin
│   │   └── websocket.py         # /api/v1/ws/public e /api/v1/ws/admin (+ validação de Origin)
│   ├── contexts/                # bounded contexts (DDD)
│   │   ├── __init__.py
│   │   └── health/
│   │       ├── __init__.py
│   │       ├── domain/
│   │       │   ├── __init__.py
│   │       │   ├── entities.py        # HealthReport, ComponentHealth
│   │       │   ├── value_objects.py   # HealthStatus
│   │       │   └── ports.py           # ClockPort, HealthCheckPort (Protocols)
│   │       ├── application/
│   │       │   ├── __init__.py
│   │       │   └── get_health.py      # GetHealthUseCase
│   │       ├── infrastructure/
│   │       │   ├── __init__.py
│   │       │   └── system_clock.py    # SystemClock (implementa ClockPort)
│   │       └── presentation/
│   │           ├── __init__.py
│   │           ├── schemas.py         # HealthResponse (Pydantic)
│   │           ├── dependencies.py    # providers para Depends()
│   │           ├── http.py            # build_health_router(scope)
│   │           └── ws_handlers.py     # handler de "health.ping"
│   └── scripts/
│       ├── __init__.py
│       └── export_openapi.py          # gera openapi.json (make openapi)
└── tests/
    ├── __init__.py
    ├── conftest.py              # fixtures: settings, app, client async, ws client, ALLOWED_ORIGIN
    ├── fakes.py                 # dublês das ports: FakeClock, StubCheck
    ├── unit/
    │   ├── core/                # test_config, test_dispatcher, test_logging
    │   └── contexts/health/
    │       ├── domain/          # test_entities, test_value_objects
    │       └── application/     # test_get_health
    ├── integration/
    │   ├── api/                 # test_health, test_cors, test_errors, test_request_id, test_docs
    │   └── websocket/           # test_health_ws
    └── contract/
        └── test_openapi_schema.py   # openapi.json versionado = gerado
```

> **Pacote `api` na raiz do projeto:** o código não é instalado com pip; os comandos rodam **na raiz do projeto**, que já está no caminho de import (no Docker, `PYTHONPATH=/app`). Os imports são absolutos a partir do pacote: `from api.core.scope import Scope`.

## O que vai em cada pasta

| Pasta / arquivo | Responsabilidade | Coloque aqui | Não coloque aqui |
|-----------------|------------------|--------------|------------------|
| `api/app_run.py` | Cria a aplicação (`create_app`) | Registro de middlewares, routers e handlers de erro | Regra de negócio, configuração de rota |
| `api/config.py` | Configuração (`Settings`) | Toda variável `APP_*` nova, com tipo e padrão | Leitura de `os.environ` espalhada pelo código |
| `api/container.py` | *Composition root* | Instanciar adapters e casos de uso, registrar handlers WS | Lógica — só montagem |
| `api/core/` | *Shared kernel*: transversal a todos os contexts | CORS, Swagger, logs, exceções e handlers de erro, `X-Request-ID`, `Scope`, `BaseSchema`, WebSocket, acesso ao DynamoDB | Qualquer coisa de um context específico |
| `api/routes/` | Composição por escopo | Incluir o router de um context em `public.py`/`admin.py`; endpoints WS por escopo em `websocket.py` | Implementação de endpoint (fica em `presentation/` do context) |
| `api/contexts/<ctx>/domain/` | Regras de negócio em Python puro | Entidades, value objects, *ports* (`Protocol`), exceções de negócio | FastAPI, Pydantic, boto, httpx |
| `api/contexts/<ctx>/application/` | Casos de uso | Uma classe por caso de uso (`<Verbo><Substantivo>UseCase`) | Acesso direto a banco/HTTP (usa as ports) |
| `api/contexts/<ctx>/infrastructure/` | Adapters das ports | Repositórios DynamoDB, clientes HTTP de parceiros (httpx + tenacity), relógio | Schemas da API, rotas |
| `api/contexts/<ctx>/presentation/` | Entrada HTTP/WS do context | Router factory, schemas `…Request`/`…Response`, handlers WS, `dependencies.py` | Regra de negócio; import direto de `infrastructure` |
| `api/scripts/` | Utilitários de linha de comando (`python -m api.scripts.<nome>`) | Exportar OpenAPI, criar tabelas locais, backfills | Código usado pela aplicação em runtime |
| `tests/` | Testes, espelhando `api/` | `unit/`, `integration/`, `contract/`, `fakes.py`, `conftest.py` | Código de produção |
| `config/` | Deploy/infra da plataforma | Arquivos exigidos pela plataforma de deploy | Código ou configuração lida pela aplicação (vai em `config.py` + variáveis `APP_*`) |
| `certificates/` | Certificados de CA adicionais | `.crt` públicos | Chaves privadas, segredos |
| `requirements*.txt` | Dependências ([13](./13-dependencias.md)) | Libs com versão fixada | — |
| `.github/` | Configuração do GitHub Copilot ([14](./14-ia-copilot.md)) | Instruções, prompts e agentes | Qualquer outra configuração |

### Onde colocar algo novo

| Preciso de… | Onde |
|-------------|------|
| Um novo assunto de negócio (ex.: parceiros) | Novo context em `api/contexts/<nome>/` — checklist em [docs/README](./README.md#checklist-para-criar-um-novo-context) |
| Um endpoint novo | `presentation/http.py` do context + inclusão em `api/routes/public.py` e/ou `admin.py` |
| Uma mensagem WebSocket nova | Handler em `presentation/ws_handlers.py` do context + `dispatcher.register(...)` no `container.py` |
| Chamar a API de um parceiro | Port no `domain/ports.py` + adapter com httpx em `infrastructure/` |
| Persistir dados | Port `…Repository` no `domain` + adapter DynamoDB em `infrastructure/` ([12](./12-persistencia-dynamodb.md)) |
| Uma variável de ambiente | Campo no `Settings` (`api/config.py`) + `.env.example` + tabela em [08](./08-docker.md#4-variáveis-de-ambiente) |
| Um erro de negócio | Subclasse de `DomainError` em `domain/errors.py` do context ([07](./07-erros-logging.md#exceções-de-negócio)) |
| Uma lib nova | [13 — Dependências](./13-dependencias.md#4-adicionar-ou-atualizar-uma-dependência) |

## Pastas da plataforma

| Pasta | Conteúdo | Regra |
|-------|----------|-------|
| `config/` | Arquivos de deploy/infra usados pela plataforma | Não mudar nome nem estrutura; a aplicação não lê esta pasta |
| `certificates/` | Certificados de CA adicionais (`.crt`) | Só certificados públicos; nunca chaves privadas |

## Arquivos gerados

| Arquivo | Gerado por | Versionado? |
|---------|-----------|-------------|
| `openapi.json` | `make openapi` | ✅ (o diff mostra mudanças de contrato no MR) |
| `.venv/` | `make install` (ou criar e ativar o venv e `pip install -r requirements-test.txt` — [11](./11-comandos.md)) | ❌ |
| `.coverage`, `htmlcov/`, `coverage.xml` | coverage | ❌ |
