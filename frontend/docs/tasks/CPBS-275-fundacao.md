# CPBS-275 — Fundação do projeto (frontend)

| Campo | Valor |
|-------|-------|
| Ticket | CPBS-275 |
| Projeto | Frontend |
| Status | Documentação concluída · implementação pendente |

## Enunciado

Criar a fundação do Bot Varejo — plataforma de atendimento, via chat, de serviços de parceiros de varejo: um **backend** em Python (FastAPI, async, WebSockets) e um **frontend** Next.js usado como SPA com as áreas web e admin, organizado por features e componentes. A entrega inclui health check nos escopos `admin` e `public`, comunicação funcionando entre frontend e backend, README com passo a passo para rodar localmente e docker compose subindo a aplicação.

## Objetivo neste projeto

Criar a **fundação do app**: estrutura por áreas e features, padrões, empacotamento Docker e uma **tela de status** em cada área, consumindo o health da API (em outro domínio) via HTTP e WebSocket.

## Critérios de aceitação

| # | Critério | Onde está documentado |
|---|----------|------------------------|
| 1 | Estrutura de pastas do projeto | [02 — Estrutura](../02-estrutura.md) |
| 2 | Comunicação com o health dos escopos `public` e `admin` | [07 — Integração com a API](../07-integracao-api.md) · [08 — Feature health](../08-feature-health.md) |
| 3 | README com passo a passo para rodar localmente | [README do frontend](../../README.md) |
| 4 | Docker Compose subindo o app | [10 — Docker](../10-docker.md) |

## Definição de pronto (DoD)

- [ ] `docker compose up --build` sobe o front em `http://localhost:3000`.
- [ ] `/health` (web) mostra o status do escopo `public` via HTTP e WebSocket.
- [ ] `/admin/health` (admin) mostra o status do escopo `admin` via HTTP e WebSocket.
- [ ] URL da API configurada **em runtime** (`API_URL`, `WS_URL`) — mesma imagem em qualquer ambiente.
- [ ] `GET /healthz` do próprio front responde 200 (HEALTHCHECK do container).
- [ ] Toda feature, rota e tela com teste; cobertura ≥ 80%; E2E das duas telas de status.
- [ ] `eslint` (incluindo fronteiras entre áreas/features), `prettier --check` e `tsc` sem erros.

## Fora de escopo

- Autenticação da área admin (o `/admin` **ainda não** é protegido).
- Chat, fluxos, integrações e demais features de negócio.
- Design system completo (só os componentes necessários para o status).
- Infra de produção: domínio, TLS, CDN.

## Decisões registradas

| ADR | Decisão |
|-----|---------|
| [ADR-0001](../adr/0001-nextjs-padrao-como-spa.md) | Next.js padrão usado como SPA |
| [ADR-0002](../adr/0002-app-unico-areas-e-features.md) | App único com áreas e features |
| [ADR-0003](../adr/0003-imagem-node.md) | Imagem node:24-slim |
| [ADR-0004](../adr/0004-config-em-runtime.md) | Config da API em runtime |
| [ADR-0005](../adr/0005-pnpm.md) | pnpm |
| [ADR-0006](../adr/0006-convencao-de-nomes.md) | camelCase |
| [ADR-0007](../adr/0007-cliente-tipado-openapi.md) | Cliente tipado do OpenAPI |
| [ADR-0008](../adr/0008-branches-e-fluxo-de-publicacao.md) | Branches e fluxo de publicação |

## Entregáveis

- Documentação do projeto: [docs/README.md](../README.md)
- Passo a passo para rodar localmente: [README.md](../../README.md)
- Padrão de branches, commits e MRs: [CONTRIBUTING.md](../../CONTRIBUTING.md) e templates em `.gitlab/merge_request_templates/`
