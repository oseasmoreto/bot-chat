# ADR-0002 — Um único app com áreas (web/admin) e features

- **Status:** Aceito
- **Data:** 2026-09-29

## Contexto
O frontend atende dois públicos — cliente final (**web**) e operação (**admin**) — num único domínio. Requisitos: modularidade, componentização e poder mexer numa feature (ou numa área) sem afetar as demais.

## Decisão
- **Um único app Next.js** com duas áreas: **web** em `/` (route group `(web)`) e **admin** em `/admin`. Um processo, uma imagem, um domínio.
- `src/app/` — rotas finas; `(web)/` para a área web e `admin/` para a área admin.
- `src/areas/{web,admin}/` — shell e features **exclusivas** de cada área.
- `src/features/` — features usadas pelas **duas** áreas, parametrizadas (ex.: `scope`).
- `src/shared/` — infraestrutura técnica sem regra de negócio (ui, api, ws, config, providers).
- Fronteiras garantidas por `eslint-plugin-boundaries`: web ↛ admin, admin ↛ web, feature ↛ feature, shared ↛ features/areas; import de feature só pelo `index.ts`.

## Alternativas consideradas
- **Features todas numa pasta só** (sem áreas): perderia a separação web × admin.
- **Feature-Sliced Design completo:** mais camadas do que precisamos agora.

## Consequências
- Remover uma feature = apagar a pasta e a rota.
- O isolamento entre web e admin é garantido por organização de pastas + lint; o Next ainda divide o JavaScript por rota.
- Extrair web e admin para apps separados no futuro continua viável: cada área já é autocontida.
