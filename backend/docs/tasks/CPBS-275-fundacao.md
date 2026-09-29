# CPBS-275 — Fundação do projeto (backend)

| Campo | Valor |
|-------|-------|
| Ticket | CPBS-275 |
| Projeto | Backend |
| Status | Documentação concluída · implementação pendente |

## Enunciado

Criar a fundação do Bot Varejo — plataforma de atendimento, via chat, de serviços de parceiros de varejo: um **backend** em Python (FastAPI, async, WebSockets) que será a base para construir fluxos e integrações, e um **frontend** Next.js usado como SPA com as áreas web e admin. A entrega inclui health check nos escopos `admin` e `public`, comunicação funcionando entre frontend e backend, README com passo a passo para rodar localmente e docker compose subindo a aplicação.

## Objetivo neste projeto

Criar a **fundação da API**: estrutura, padrões, empacotamento Docker e um *health check* por escopo, via HTTP e WebSocket, consumido pelo frontend em outro domínio.

## Critérios de aceitação

| # | Critério | Onde está documentado |
|---|----------|------------------------|
| 1 | Estrutura de pastas do projeto | [02 — Estrutura](../02-estrutura.md) |
| 2 | Health check para os escopos `admin` e `public` | [06 — Contratos de API](../06-contratos-api.md) |
| 3 | README com passo a passo para rodar localmente | [README do backend](../../README.md) |
| 4 | Docker Compose subindo a API | [08 — Docker e deploy](../08-docker-deploy.md) |

## Definição de pronto (DoD)

- [ ] `docker compose up --build` sobe a API em `http://localhost:8000`.
- [ ] `GET /api/v1/public/health` e `GET /api/v1/admin/health` retornam `200` com o schema documentado.
- [ ] `ws://localhost:8000/api/v1/ws/public` e `/api/v1/ws/admin` respondem `health.ping` com `health.pong` (com `Origin` permitido).
- [ ] CORS liberado apenas para as origens de `APP_CORS_ORIGINS`.
- [ ] Swagger em `/api/docs` e OpenAPI em `/api/openapi.json`; `openapi.json` versionado e atualizado.
- [ ] O frontend (`http://localhost:3000`) consome o health dos dois escopos via HTTP e WebSocket.
- [ ] Toda rota e mensagem WS com teste; cobertura ≥ 90%.
- [ ] `ruff`, `mypy --strict` e `lint-imports` sem erros.

## Fora de escopo

- Implementação da persistência. O banco já está definido e documentado: DynamoDB ([ADR-0009](../adr/0009-dynamodb.md), [12 — Persistência](../12-persistencia-dynamodb.md)).
- Armazenamento de arquivos.
- Autenticação/autorização (o escopo `admin` **ainda não** é protegido).
- Motor de fluxos de conversa e integrações com parceiros.
- Observabilidade avançada (métricas, tracing).
- Infra de produção: domínio, TLS, load balancer, escala horizontal.

## Decisões registradas

| ADR | Decisão |
|-----|---------|
| [ADR-0001](../adr/0001-imagem-python-uvicorn.md) | Imagem python:3.13-slim com Uvicorn |
| [ADR-0002](../adr/0002-dominio-proprio-cors.md) | Domínio próprio, prefixo /api, CORS e Origin |
| [ADR-0003](../adr/0003-ddd.md) | DDD com bounded contexts |
| [ADR-0004](../adr/0004-uv.md) | uv |
| [ADR-0005](../adr/0005-convencao-de-nomes.md) | Convenção de nomes |
| [ADR-0006](../adr/0006-contrato-openapi.md) | Contrato OpenAPI |
| [ADR-0007](../adr/0007-protocolo-websocket.md) | Protocolo WebSocket |
| [ADR-0008](../adr/0008-branches-e-fluxo-de-publicacao.md) | Branches e fluxo de publicação |

## Entregáveis

- Documentação do projeto: [docs/README.md](../README.md)
- Passo a passo para rodar localmente: [README.md](../../README.md)
- Padrão de branches, commits e MRs: [CONTRIBUTING.md](../../CONTRIBUTING.md) e templates em `.gitlab/merge_request_templates/`
