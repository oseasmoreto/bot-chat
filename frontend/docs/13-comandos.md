# 13 — Comandos (frontend)

Tudo roda **na raiz do projeto**: scripts do `package.json` (`pnpm <script>`) ou os atalhos do `Makefile`.

## 1. Scripts do `package.json`

| Script | Comando |
|--------|---------|
| `dev` | `next dev` |
| `build` | `next build` |
| `start` | `node .next/standalone/server.js` |
| `lint` | `eslint .` |
| `typecheck` | `tsc --noEmit` |
| `test` | `vitest run` |
| `e2e` | `playwright test` |
| `openapi` | baixa `/api/openapi.json` da API e gera `schema.d.ts` ([07](./07-integracao-api.md#3-cliente-http-tipado-srcsharedapi)) |

## 2. Makefile — atalhos

| Alvo | O que faz |
|------|-----------|
| `make setup` | `pnpm install` + `pre-commit install` + `git config commit.template .gitmessage` |
| `make up` | `docker compose up --build` (imagem de runtime) |
| `make down` | `docker compose down` |
| `make dev` | `docker compose -f docker-compose.dev.yml up --build` (hot reload) |
| `make run` | `API_URL=… WS_URL=… pnpm dev` (sem Docker) |
| `make lint` | `pnpm lint` + `prettier --check` |
| `make format` | `prettier --write` + `eslint --fix` |
| `make typecheck` | `pnpm typecheck` |
| `make test` | `pnpm test` com cobertura |
| `make e2e` | `pnpm e2e` contra `E2E_BASE_URL` do `.env` (front e API já no ar) |
| `make openapi` | `pnpm openapi` |
| `make build` | `docker build --target runtime -t bot-varejo-web:local .` |

## 3. E2E contra outro ambiente

Os E2E nunca sobem front, API ou banco: testam o front que está em `E2E_BASE_URL` ([11 — Testes](./11-testes.md#playwrightconfigts)). Para validar um ambiente implantado, aponte a variável para ele:

```bash
E2E_BASE_URL=https://app-dev.<dominio> pnpm e2e
```
