# Documentação — Backend

> Projeto `backend/` do Bot Varejo
> Frontend: `docs/README.md` no repositório do **frontend** · Branch/commit/MR: [CONTRIBUTING.md](../CONTRIBUTING.md) · Templates de MR: [`.gitlab/merge_request_templates/`](../.gitlab/merge_request_templates)

API REST + WebSocket em **Python 3.13 + FastAPI**, servida em domínio próprio (`api.<dominio>`), para os escopos `public` e `admin`.

## Índice

| # | Documento | Conteúdo |
|---|-----------|----------|
| 00 | [Visão geral](./00-visao-geral.md) | Contexto, stack, princípios |
| 01 | [Arquitetura](./01-arquitetura.md) | Contexto do sistema, containers, rotas, fluxos HTTP/WS, evolução |
| 02 | [Estrutura de pastas](./02-estrutura.md) | Árvore do projeto, o que vai em cada pasta, onde colocar algo novo, arquivos gerados |
| 03 | [Arquitetura DDD](./03-arquitetura-ddd.md) | Bounded contexts, camadas, regra de dependência, SOLID/DRY/KISS |
| 04 | [Context `health`](./04-context-health.md) | Código de referência completo, incluindo `app_run.py` com CORS |
| 05 | [WebSocket](./05-websocket.md) | Validação de `Origin`, dispatcher, handlers |
| 06 | [Contratos de API](./06-contratos-api.md) | URLs, endpoints, schemas, CORS, protocolo WS, evolução do contrato, OpenAPI |
| 07 | [Erros e logging](./07-erros-logging.md) | Formato de erro, log estruturado, `X-Request-ID` |
| 08 | [Docker e deploy](./08-docker-deploy.md) | Dockerfile, compose, variáveis de ambiente |
| 09 | [Testes](./09-testes.md) | TDD, matriz obrigatória, exemplos (unitário, rota, CORS, WS, contrato, smoke) |
| 10 | [Padrões de código](./10-padroes-codigo.md) | Nomenclatura, convenções de API, tipagem, lint, `pyproject.toml` |
| 11 | [CI e comandos](./11-ci.md) | Pipeline por ambiente (developer, staging, master), deploy, Makefile |
| 12 | [Persistência (DynamoDB)](./12-persistencia-dynamodb.md) | Tabela por context, chaves e índices, repositórios, config, ambiente local, testes |
| 13 | [Dependências](./13-dependencias.md) | `requirements.txt` e `requirements-test.txt`: cada lib, para que serve, onde pode ser usada, como adicionar/atualizar |
| 14 | [IA — GitHub Copilot](./14-ia-copilot.md) | Instruções, prompts e agente do Copilot no VS Code para criar contexts, módulos e APIs |
| — | [Tarefas](./tasks/README.md) | Objetivo, critérios de aceitação e escopo de cada tarefa |
| — | [ADRs](./adr/README.md) | Decisões de arquitetura do backend |
| — | [Glossário](./glossario.md) | Termos de negócio e técnicos |

## Endpoints

| Tipo | Path | Escopo |
|------|------|--------|
| REST | `GET /api/v1/public/health` | public |
| REST | `GET /api/v1/admin/health` | admin |
| WebSocket | `/api/v1/ws/public` | public |
| WebSocket | `/api/v1/ws/admin` | admin |
| Docs | `/api/docs`, `/api/redoc`, `/api/openapi.json` | — |

## Checklist para criar um novo context

No VS Code, o prompt `/novo-context` do Copilot executa este checklist ([14 — IA](./14-ia-copilot.md)).


1. `contexts/<nome>/{domain,application,infrastructure,presentation}/` com `__init__.py`.
2. Escrever os testes de domínio e caso de uso **primeiro** (TDD).
3. Declarar ports em `domain/ports.py`; implementar em `infrastructure/`.
4. Registrar no `container.py`.
5. Criar `build_<nome>_router(scope)` (se exposto nos dois escopos) ou router dedicado, e incluir em `routes/public.py` e/ou `routes/admin.py`.
6. Rodar `lint-imports` — os contratos já cobrem `api.contexts.*`.
7. Teste de integração para cada rota; `make openapi` para atualizar `openapi.json`.
8. Documentar endpoints em [06 — Contratos de API](./06-contratos-api.md) e avisar o frontend (ticket/MR vinculado).

## Como manter esta documentação

1. Mudança só do backend → atualize esta pasta.
2. Mudança de contrato → [06](./06-contratos-api.md) + `openapi.json` + ticket no frontend.
3. Nova decisão → novo ADR; decisão alterada → reescreva o ADR com a decisão vigente. A documentação descreve só o estado atual — histórico fica no git.
4. Diagramas em **Mermaid**, versionados e revisados em MR como código.
