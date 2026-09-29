# 00 — Visão geral e escopo (frontend)

> Task de origem: **CPBS-275** — fundação do projeto de atendimento de serviços de parceiros de varejo via chat.

## Contexto

O **Bot Varejo** é a plataforma de atendimento, via chat, de serviços oferecidos por parceiros de varejo. O sistema tem dois projetos independentes, cada um com repositório, documentação e deploy próprios:

| Projeto | Domínio | Responsabilidade |
|---------|---------|------------------|
| **Frontend** (este) | `app.<dominio>` | App Next.js com as áreas **web** (`/`) e **admin** (`/admin`) |
| Backend | `api.<dominio>` | APIs REST e WebSocket dos escopos `public` e `admin` |

O frontend é **um único app Next.js** com duas áreas:

| Área | URL | Escopo da API | Público | Exemplo de uso futuro |
|------|-----|---------------|---------|------------------------|
| **web** | `/` | `public` | Cliente final do parceiro | Conversar com o bot, contratar/consultar serviços |
| **admin** | `/admin` | `admin` | Operadores, time interno, parceiros | Construir fluxos, configurar integrações, acompanhar atendimentos |

## Objetivo da CPBS-275 (parte frontend)

Criar a **fundação do app**: estrutura por áreas e features, padrões, empacotamento Docker e uma **tela de status** em cada área, consumindo o health da API (em outro domínio) via HTTP e WebSocket.

## Stack

| Item | Tecnologia |
|------|------------|
| Runtime | Node.js 24 LTS |
| Framework | Next.js (App Router), **servidor padrão** (`output: 'standalone'`), usado como **SPA** |
| UI | React + TypeScript (`strict`) + Tailwind CSS v4 |
| Dados | TanStack Query (estado de servidor) · `openapi-fetch` + `openapi-typescript` (cliente tipado) |
| Tempo real | WebSocket nativo do navegador (cliente próprio em `shared/ws`) |
| Dependências | pnpm |
| Qualidade | ESLint (flat config, `eslint-plugin-boundaries`), Prettier |
| Testes | Vitest, Testing Library, MSW, Playwright |
| Container | Imagem `node:24-slim` rodando `node server.js` |

## Critérios de aceitação (parte frontend)

| # | Critério | Onde está documentado |
|---|----------|------------------------|
| 1 | Estrutura de pastas do projeto | [02 — Estrutura](./02-estrutura.md) |
| 2 | Comunicação com o health dos escopos `public` e `admin` | [07 — Integração com a API](./07-integracao-api.md) · [08 — Feature health](./08-feature-health.md) |
| 3 | README com passo a passo para rodar localmente | [README do frontend](../README.md) |
| 4 | Docker Compose subindo o app | [10 — Docker e deploy](./10-docker-deploy.md) |

### Definição de pronto (DoD)

- [ ] `docker compose up --build` sobe o front em `http://localhost:3000`.
- [ ] `/health` (web) mostra o status do escopo `public` via HTTP e WebSocket.
- [ ] `/admin/health` (admin) mostra o status do escopo `admin` via HTTP e WebSocket.
- [ ] URL da API configurada **em runtime** (`API_URL`, `WS_URL`) — mesma imagem em qualquer ambiente.
- [ ] `GET /healthz` do próprio front responde 200 (HEALTHCHECK do container).
- [ ] Toda feature, rota e tela com teste; cobertura ≥ 80%; E2E das duas telas de status.
- [ ] `eslint` (incluindo fronteiras entre áreas/features), `prettier --check` e `tsc` sem erros.

## Fora de escopo (nesta task)

- Autenticação da área admin (o `/admin` **ainda não** é protegido).
- Chat, fluxos, integrações e demais features de negócio.
- Design system completo (só os componentes necessários para o status).
- Infra de produção: domínio, TLS, CDN.

## Princípios

| Princípio | Como se aplica no frontend |
|-----------|----------------------------|
| **Modularidade** | Áreas (web/admin) e features isoladas; mexer em uma não afeta as outras — garantido por lint |
| **Componentização** | UI reutilizável em `shared/ui`; features compõem componentes |
| **DRY** | Features comuns às duas áreas em `features/`; cliente HTTP/WS e tipos gerados em `shared/` |
| **KISS** | Um app, um processo, uma imagem; SPA simples com TanStack Query |
| **TDD** | Teste antes do código; nenhuma feature/rota/tela sem teste |
| **Tipagem forte** | TS `strict`, tipos da API gerados do OpenAPI do backend |
