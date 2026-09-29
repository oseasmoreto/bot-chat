# ADR-0003 — Imagem node:24-slim rodando o servidor Next

- **Status:** Aceito
- **Data:** 2026-09-29

## Decisão
- Dockerfile multi-stage (`deps`, `dev`, `builder`, `runtime`) em `node:24-slim`.
- Imagem final com o output `standalone` do Next (`node server.js`), usuário `node`, porta 3000, HEALTHCHECK em `/healthz`.
- Um processo por container; TLS e domínio na plataforma de deploy.

## Alternativas consideradas
- **Imagem Alpine:** `slim` (glibc) evita incompatibilidades de binários nativos (SWC, sharp).

## Consequências
- Escala por réplicas.
- Imagem enxuta: sem pnpm nem dependências de build.
