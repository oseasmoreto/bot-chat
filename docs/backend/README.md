# Backend

**Pasta no repositório:** `backend/`
**Stack:** Python 3.13 · FastAPI · Uvicorn · Pydantic v2 · pydantic-settings · async/await · WebSockets
**Ferramentas:** uv · ruff (lint + format) · mypy `--strict` · import-linter · pytest + pytest-asyncio + httpx · coverage

> O backend **só** expõe APIs REST (`/api/*`) e WebSocket (`/ws/*`) para os dois escopos (`public` e `admin`). Arquivos estáticos e roteamento são responsabilidade do Nginx ([ADR-0002](../adr/0002-imagem-unica-nginx-uvicorn.md)).

## Documentos

| # | Documento | Conteúdo |
|---|-----------|----------|
| 01 | [Estrutura de pastas](./01-estrutura.md) | Árvore de `backend/` e responsabilidade de cada arquivo |
| 02 | [Arquitetura DDD](./02-arquitetura-ddd.md) | Bounded contexts, camadas, regra de dependência, SOLID/DRY/KISS |
| 03 | [Context `health`](./03-context-health.md) | Código de referência completo: domínio → caso de uso → router |
| 04 | [WebSocket](./04-websocket.md) | Endpoints, dispatcher de mensagens, handlers |
| 05 | [Contratos de API](./05-contratos-api.md) | Endpoints REST, schemas, protocolo WS, OpenAPI/Swagger |
| 06 | [Erros e logging](./06-erros-logging.md) | Formato de erro, log estruturado, `X-Request-ID` |
| 07 | [Testes](./07-testes.md) | Fakes, fixtures, testes unitários, de rota, WS e contrato |
| 08 | [Padrões Python](./08-padroes-python.md) | Nomenclatura, tipagem, boas práticas, `pyproject.toml` |

## Endpoints desta fase (CPBS-275)

| Tipo | Path | Escopo |
|------|------|--------|
| REST | `GET /api/v1/public/health` | public |
| REST | `GET /api/v1/admin/health` | admin |
| WebSocket | `/ws/public` | public |
| WebSocket | `/ws/admin` | admin |
| Docs | `/api/docs`, `/api/redoc`, `/api/openapi.json` | — |

Detalhes em [Contratos de API](./05-contratos-api.md).

## Comandos

| Ação | Comando (dentro de `backend/`) |
|------|--------------------------------|
| Instalar deps | `uv sync` |
| Rodar em dev | `uv run uvicorn bot_varejo.main:create_app --factory --reload --port 8000` |
| Testes | `uv run pytest` |
| Lint | `uv run ruff check .` |
| Formatar | `uv run ruff format .` |
| Tipos | `uv run mypy src tests` |
| Fronteiras | `uv run lint-imports` |
| Exportar OpenAPI | `uv run python -m bot_varejo.scripts.export_openapi ../packages/api-client/openapi.json` |

## Checklist para criar um novo context

1. `contexts/<nome>/{domain,application,infrastructure,presentation}/` com `__init__.py`.
2. Escrever os testes de domínio e caso de uso **primeiro** (TDD).
3. Declarar ports em `domain/ports.py`; implementar em `infrastructure/`.
4. Registrar no `container.py`.
5. Criar `build_<nome>_router(scope)` (se exposto nos dois escopos) ou router dedicado, e incluir em `api/public.py` e/ou `api/admin.py`.
6. Adicionar o context no contrato do import-linter.
7. Teste de integração para cada rota; regenerar OpenAPI (`make openapi`).
8. Documentar endpoints em [Contratos de API](./05-contratos-api.md).
