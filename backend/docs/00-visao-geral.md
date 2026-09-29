# 00 — Visão geral e escopo (backend)

> Task de origem: **CPBS-275** — fundação do projeto de atendimento de serviços de parceiros de varejo via chat.

## Contexto

O **Bot Varejo** é a plataforma de atendimento, via chat, de serviços oferecidos por parceiros de varejo. O sistema tem dois projetos independentes, cada um com repositório, documentação e deploy próprios:

| Projeto | Domínio | Responsabilidade |
|---------|---------|------------------|
| **Backend** (este) | `api.<dominio>` | APIs REST e WebSocket para os escopos `public` e `admin`; base para fluxos e integrações |
| Frontend | `app.<dominio>` | App Next.js com as áreas web (`/`) e admin (`/admin`) |

O backend atende dois **escopos**:

| Escopo | Consumidor | Exemplo de uso futuro |
|--------|------------|------------------------|
| `public` | Área web do frontend (cliente final) | Conversar com o bot, contratar/consultar serviços |
| `admin` | Área admin do frontend (operadores, parceiros) | Construir fluxos, configurar integrações, acompanhar atendimentos |

## Objetivo da CPBS-275 (parte backend)

Criar a **fundação da API**: estrutura, padrões, empacotamento Docker e um *health check* por escopo, via HTTP e WebSocket, consumido pelo frontend em outro domínio.

## Stack

| Item | Tecnologia |
|------|------------|
| Linguagem | Python 3.13 |
| Framework | FastAPI (async) + Uvicorn |
| Tempo real | WebSockets (Starlette/FastAPI) |
| Validação / schemas | Pydantic v2, pydantic-settings |
| Dependências | uv |
| Qualidade | ruff, mypy `--strict`, import-linter |
| Testes | pytest, pytest-asyncio, httpx |
| Container | Imagem `python:3.13-slim`, Uvicorn direto |
| Documentação da API | OpenAPI 3.1 + Swagger UI (`/api/docs`) + ReDoc (`/api/redoc`) |

## Critérios de aceitação (parte backend)

| # | Critério | Onde está documentado |
|---|----------|------------------------|
| 1 | Estrutura de pastas do projeto | [02 — Estrutura](./02-estrutura.md) |
| 2 | Health check para os escopos `admin` e `public` | [06 — Contratos de API](./06-contratos-api.md) |
| 3 | README com passo a passo para rodar localmente | [README do backend](../README.md) |
| 4 | Docker Compose subindo a API | [08 — Docker e deploy](./08-docker-deploy.md) |

### Definição de pronto (DoD)

- [ ] `docker compose up --build` sobe a API em `http://localhost:8000`.
- [ ] `GET /api/v1/public/health` e `GET /api/v1/admin/health` retornam `200` com o schema documentado.
- [ ] `ws://localhost:8000/api/v1/ws/public` e `/api/v1/ws/admin` respondem `health.ping` com `health.pong` (com `Origin` permitido).
- [ ] CORS liberado apenas para as origens de `APP_CORS_ORIGINS`.
- [ ] Swagger em `/api/docs` e OpenAPI em `/api/openapi.json`; `openapi.json` versionado e atualizado.
- [ ] O frontend (`http://localhost:3000`) consome o health dos dois escopos via HTTP e WebSocket.
- [ ] Toda rota e mensagem WS com teste; cobertura ≥ 90%.
- [ ] `ruff`, `mypy --strict` e `lint-imports` sem erros.

## Fora de escopo (nesta task)

- Banco de dados e persistência.
- Armazenamento de arquivos.
- Autenticação/autorização (o escopo `admin` **ainda não** é protegido).
- Motor de fluxos de conversa e integrações com parceiros.
- Observabilidade avançada (métricas, tracing).
- Infra de produção: domínio, TLS, load balancer, escala horizontal.

## Princípios

| Princípio | Como se aplica no backend |
|-----------|---------------------------|
| **DDD** | Bounded contexts; domínio sem dependência de framework |
| **SOLID** | Casos de uso com responsabilidade única; dependências por `Protocol` |
| **DRY** | Router factory por escopo; `BaseSchema` central; handlers WS reutilizam casos de uso |
| **KISS** | Sem DI framework, sem ORM, sem broker nesta fase |
| **TDD** | Teste antes do código; nenhuma rota/mensagem sem teste |
| **Tipagem forte** | `mypy --strict`, Pydantic, contrato OpenAPI gerado |
