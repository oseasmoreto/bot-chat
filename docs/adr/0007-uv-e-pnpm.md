# ADR-0007 — uv e pnpm como gerenciadores

- **Status:** Aceito
- **Data:** 2026-09-29
- **Ticket:** CPBS-275

## Decisão
- **Python:** `uv` (dependências, lockfile `uv.lock`, venv, execução). Ferramentas: ruff, mypy, pytest.
- **Node:** `pnpm` com workspaces (via corepack). Ferramentas: ESLint, Prettier, Vitest, Testing Library, MSW, Playwright.
- Versões de runtime: Python 3.13 (`.python-version`), Node 24 LTS (`.nvmrc`).

## Alternativas consideradas
- **Poetry / pip-tools:** mais lentos; uv cobre instalação, lock e execução em uma ferramenta.
- **npm / yarn:** pnpm tem workspaces maduros, instalação rápida e `node_modules` estrito (evita dependências fantasmas).
- **Jest:** Vitest é mais rápido e nativo em ESM/TS.

## Consequências
- Instalação local exige `uv` e `corepack enable` (README).
- Lockfiles sempre commitados; CI usa `--frozen` / `--frozen-lockfile`.
