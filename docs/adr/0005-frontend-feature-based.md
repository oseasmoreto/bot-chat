# ADR-0005 — Frontends feature-based + pacotes compartilhados

- **Status:** Aceito
- **Data:** 2026-09-29
- **Ticket:** CPBS-275

## Contexto
Requisito: poder mexer em uma feature sem interferir nas demais, com modularidade e componentização, em dois apps.

## Decisão
- Cada app: `src/app` (rotas finas), `src/features/<feature>` (isoladas, API pública via `index.ts`), `src/shared` (infra do app).
- Features não importam outras features; garantido por `eslint-plugin-boundaries`.
- Código comum aos dois apps em `packages/`: `ui`, `api-client`, `ws-client`, `config`.
- Pacotes consumidos como fonte TS via `transpilePackages` (sem build próprio).

## Alternativas consideradas
- **Estrutura por tipo** (`components/`, `hooks/`, `services/` globais): acoplamento implícito entre features.
- **Feature-Sliced Design completo:** mais camadas (entities, widgets, processes) do que precisamos agora.

## Consequências
- Remover uma feature = apagar a pasta e a rota.
- Duplicação pontual entre apps é aceita até a "regra de três"; depois vira `packages/feature-*`.
