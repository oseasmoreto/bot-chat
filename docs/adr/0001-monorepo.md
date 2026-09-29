# ADR-0001 — Monorepo com pnpm workspaces + projeto Python

- **Status:** Aceito
- **Data:** 2026-09-29
- **Ticket:** CPBS-275

## Contexto
O produto tem um backend Python e dois frontends Next.js que compartilham UI, cliente de API e configurações. A entrega é **um único deploy**.

## Decisão
Um único repositório com:
- `backend/` — projeto Python independente (uv).
- `web/`, `admin/` e `packages/*` — workspace pnpm.
- `infra/` — Dockerfile, Nginx, supervisord.
- `docs/` — documentação e ADRs.

## Alternativas consideradas
- **Um repositório por app:** duplicaria UI/cliente, dificultaria mudanças de contrato atômicas (backend + front no mesmo PR) e contraria o deploy único.
- **Turborepo/Nx:** úteis em escala, mas adicionam complexidade agora (KISS). Podem ser adotados depois sem mudar a estrutura de pastas.

## Consequências
- Mudança de contrato (backend + `openapi.json` + front) acontece em um único PR.
- Regras de fronteira entre pastas precisam de lint (ver [02 — Estrutura do repositório](../02-estrutura-repositorio.md) e [frontend-comum — feature-based](../frontend-comum/02-arquitetura-feature-based.md)).
- CI roda backend e frontend em paralelo.
