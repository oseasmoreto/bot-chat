# 00 — Visão geral e escopo

## Contexto

O **Bot Varejo** é a plataforma de atendimento, via chat, de serviços oferecidos por parceiros de varejo. A plataforma terá dois públicos:

| Escopo | Aplicação | Público | Exemplo de uso futuro |
|--------|-----------|---------|------------------------|
| **public** | `web/` | Cliente final do parceiro | Conversar com o bot, contratar/consultar um serviço |
| **admin** | `admin/` | Operadores, time interno, parceiros | Construir fluxos de conversa, configurar integrações, acompanhar atendimentos |

Ambos compartilham **um único backend** (`backend/`), que será a base para construir **fluxos** (roteiros de conversa) e **integrações** (APIs de parceiros).

## Objetivo da CPBS-275

Criar a **fundação** do projeto: estrutura de repositório, padrões, empacotamento e um *health check* funcional em cada escopo, provando que **frontends ↔ Nginx ↔ backend** se comunicam via HTTP e WebSocket.

> Esta etapa é **apenas documentação e diagramas**. A implementação vem em seguida, seguindo exatamente o que está descrito aqui.

## Stack

| Camada | Tecnologia | Observação |
|--------|------------|------------|
| Backend | Python 3.13, FastAPI, async/await, WebSockets, Pydantic v2 | Apenas APIs REST e WebSocket — **não serve arquivos estáticos** |
| Frontends | Next.js (App Router) em modo **SPA / static export**, React, TypeScript, Tailwind CSS | Dois apps: `web` e `admin` |
| Roteamento | Nginx | Serve os builds estáticos e faz proxy de `/api` e `/ws` |
| Empacotamento | Docker — **imagem única** com Nginx + Uvicorn (supervisord) | Um único deploy |
| Orquestração local | Docker Compose | `docker compose up` sobe a aplicação completa |
| Gerenciadores | `uv` (Python), `pnpm` workspaces (Node) | Ver [ADR-0007](./adr/0007-uv-e-pnpm.md) |

## Critérios de aceitação (CPBS-275)

| # | Critério | Onde está documentado |
|---|----------|------------------------|
| 1 | Estruturação de pastas do repositório | [02 — Estrutura do repositório](./02-estrutura-repositorio.md) |
| 2 | Endpoint de health check para os 2 escopos (admin, public) | [backend — Contratos de API](./backend/05-contratos-api.md) |
| 3 | README com passo a passo para rodar localmente | [README da raiz](../README.md) |
| 4 | Docker Compose subindo a aplicação | [04 — Docker e deploy](./04-docker-deploy.md) |

### Definição de pronto (DoD) da implementação

- [ ] `docker compose up --build` sobe a aplicação em `http://localhost:8080`.
- [ ] `GET /api/v1/public/health` e `GET /api/v1/admin/health` retornam `200` com o schema documentado.
- [ ] `ws://localhost:8080/ws/public` e `/ws/admin` respondem `health.ping` com `health.pong`.
- [ ] `http://localhost:8080/` (web) e `http://localhost:8080/admin/` (admin) exibem uma tela de status consumindo o health via HTTP **e** WebSocket.
- [ ] Swagger disponível em `/api/docs` e OpenAPI em `/api/openapi.json`.
- [ ] Toda rota, feature e tela criada possui teste; pipeline de testes verde.
- [ ] Lint, formatação e checagem de tipos sem erros (`ruff`, `mypy --strict`, `eslint`, `tsc`).

## Fora de escopo (nesta task)

Registrado para não haver ambiguidade — cada item vira uma task futura:

- Banco de dados e persistência.
- Armazenamento de arquivos.
- Autenticação/autorização (o escopo `admin` **ainda não** é protegido).
- Motor de fluxos de conversa e integrações com parceiros.
- Observabilidade avançada (métricas, tracing).
- Infra de produção (TLS, domínio, CDN, escala horizontal).

## Princípios que guiam todo o projeto

| Princípio | Como se aplica |
|-----------|----------------|
| **DDD** | Backend organizado por *bounded contexts*, domínio sem dependência de framework |
| **SOLID** | Casos de uso com responsabilidade única, dependências por abstração (`Protocol`) |
| **DRY** | Pacotes compartilhados entre fronts; router factory por escopo no backend; tipos gerados do OpenAPI |
| **KISS** | Sem abstrações antecipadas; só o necessário para o health funcionar ponta a ponta |
| **TDD** | Teste escrito antes da implementação; nenhuma rota/tela/feature sem teste |
| **Tipagem forte** | `mypy --strict` no backend, `strict: true` no TypeScript, contratos gerados |
| **Modularidade** | Frontends *feature-based*: mexer em uma feature não afeta as demais |
