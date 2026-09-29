# Frontend comum (web + admin)

O que vale **para os dois frontends**: stack, arquitetura, pacotes compartilhados (`packages/`), padrões e infraestrutura de testes. O que é específico de cada app está em [`../web/`](../web/README.md) e [`../admin/`](../admin/README.md).

**Stack:** Next.js (App Router) em modo **static export (SPA)** · React · TypeScript (`strict`) · Tailwind CSS v4
**Dados:** TanStack Query (estado de servidor) · `openapi-fetch` + `openapi-typescript` (cliente HTTP tipado)
**Testes:** Vitest · Testing Library · MSW · Playwright
**Qualidade:** ESLint (flat config) · Prettier · `eslint-plugin-boundaries`

| App | Pasta | Escopo | Servido em | `basePath` | Documentação |
|-----|-------|--------|------------|------------|--------------|
| Web | `web/` | public | `/` | — | [web/](../web/README.md) |
| Admin | `admin/` | admin | `/admin` | `/admin` | [admin/](../admin/README.md) |

## Documentos

| # | Documento | Conteúdo |
|---|-----------|----------|
| 01 | [Next.js static export](./01-nextjs-static-export.md) | Por que SPA estática, limitações, `next.config.ts` |
| 02 | [Arquitetura feature-based](./02-arquitetura-feature-based.md) | Regras de isolamento, anatomia de feature, lint de fronteiras |
| 03 | [Pacotes compartilhados](./03-pacotes-compartilhados.md) | `ui`, `api-client`, `ws-client`, `config` |
| 04 | [Estilo e TypeScript](./04-estilo-e-typescript.md) | Tailwind v4, tema, `tsconfig` base |
| 05 | [Padrões TypeScript/React](./05-padroes-typescript.md) | Nomenclatura (camelCase), tipagem, boas práticas, imports |
| 06 | [Testes](./06-testes.md) | Setup Vitest, MSW, `renderWithProviders`, factories, E2E |

## Comandos

| Ação | Comando (na raiz) |
|------|-------------------|
| Instalar | `pnpm install` |
| Dev web | `pnpm --filter web dev` (porta 3000) |
| Dev admin | `pnpm --filter admin dev` (porta 3001) |
| Build | `pnpm --filter web build && pnpm --filter admin build` |
| Testes unitários | `pnpm -r test` |
| E2E | `pnpm --filter web e2e` / `pnpm --filter admin e2e` |
| Lint | `pnpm -r lint` |
| Tipos | `pnpm -r typecheck` |
| Gerar cliente | `make openapi` |

> Em dev, acesse **sempre pelo Nginx** (`http://localhost:8080` e `/admin`) via `docker-compose.dev.yml`, para que `/api` e `/ws` funcionem na mesma origem. Ver [04 — Docker §3](../04-docker-deploy.md#3-docker-compose).

## Checklist para criar uma nova feature

1. `src/features/<nome>/` com `index.ts`.
2. Escrever teste do componente/hook **antes** (TDD) com MSW mockando a API.
3. `api/` usando `apiClient` (se o endpoint não existe no contrato, ele primeiro nasce no backend + `make openapi`).
4. Exportar só o necessário no `index.ts`.
5. Criar a rota em `src/app/<rota>/page.tsx` apenas compondo a feature.
6. Teste da rota (render da page) + cenário E2E se for uma tela nova.
7. Lint de fronteiras verde.
