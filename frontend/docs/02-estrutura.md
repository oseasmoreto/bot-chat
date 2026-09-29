# 02 — Estrutura de pastas (frontend)

O frontend é um **projeto independente**: tem seu próprio README, docs, Dockerfile, docker compose, Makefile e pipeline. Nada aqui depende do código do backend — a única ligação é o contrato HTTP/WS, consumido via `openapi.json` baixado da API ([07](./07-integracao-api.md)).

```text
frontend/
├── README.md                       # passo a passo para rodar localmente
├── CONTRIBUTING.md                 # branches, commits, MRs, versionamento, validações
├── .gitmessage                     # template de mensagem de commit
├── docs/                           # esta documentação (+ adr/, tasks/)
├── package.json                    # scripts: dev, build, start, test, e2e, lint, typecheck, openapi
├── pnpm-lock.yaml
├── .nvmrc                          # 24
├── next.config.ts                  # output: 'standalone', headers de segurança
├── tsconfig.json                   # strict + alias @/*
├── eslint.config.mjs               # regras + fronteiras entre áreas/features
├── prettier.config.mjs
├── postcss.config.mjs              # Tailwind v4
├── vitest.config.ts
├── playwright.config.ts
├── Dockerfile                      # multi-stage: deps, dev, builder, runtime (node:24-slim)
├── docker-compose.yml              # sobe a imagem de runtime (+ profile "api" com o backend)
├── docker-compose.dev.yml          # next dev com hot reload
├── Makefile
├── .env.example                    # todas as variáveis documentadas
├── .dockerignore
├── .gitlab-ci.yml                  # pipeline: validate, lint, testes, build, e2e, publish
├── .gitlab/
│   └── merge_request_templates/    # templates de MR do frontend: Default, Bugfix, Hotfix, Docs
├── scripts/
│   └── fetch-openapi.mjs           # baixa o /api/openapi.json da API para src/shared/api/
├── public/                         # favicon, imagens estáticas
├── e2e/                            # Playwright
│   ├── web/health.spec.ts
│   └── admin/health.spec.ts
└── src/
    ├── app/                        # ROTAS — só compõem; sem lógica nem fetch
    │   ├── layout.tsx              # raiz: <html>, lê config de runtime, <Providers>
    │   ├── globals.css             # Tailwind + tema
    │   ├── not-found.tsx
    │   ├── healthz/
    │   │   └── route.ts            # GET /healthz — liveness do servidor Next
    │   ├── (web)/                  # ÁREA WEB (route group: não aparece na URL)
    │   │   ├── layout.tsx          # <WebShell>
    │   │   ├── page.tsx            # /
    │   │   └── health/
    │   │       ├── page.tsx        # /health — status do escopo public
    │   │       └── page.test.tsx
    │   └── admin/                  # ÁREA ADMIN — URL /admin
    │       ├── layout.tsx          # <AdminShell>
    │       ├── page.tsx            # /admin
    │       └── health/
    │           ├── page.tsx        # /admin/health — status do escopo admin
    │           └── page.test.tsx
    ├── areas/                      # o que é EXCLUSIVO de cada área
    │   ├── web/
    │   │   ├── layout/
    │   │   │   ├── WebShell.tsx
    │   │   │   └── WebShell.test.tsx
    │   │   └── features/           # features só do web (futuro: chat/)
    │   └── admin/
    │       ├── layout/
    │       │   ├── AdminShell.tsx
    │       │   └── AdminShell.test.tsx
    │       └── features/           # features só do admin (futuro: flows/, integrations/, partners/)
    ├── features/                   # features usadas pelas DUAS áreas
    │   └── health/
    │       ├── index.ts            # API pública da feature (único ponto de import externo)
    │       ├── types.ts            # tipos derivados do OpenAPI
    │       ├── api/
    │       │   └── getHealth.ts
    │       ├── hooks/
    │       │   ├── useHealth.ts            # TanStack Query (HTTP)
    │       │   └── useHealthSocket.ts      # WebSocket ping/pong
    │       ├── components/
    │       │   ├── HealthStatusCard.tsx
    │       │   └── HealthStatusBadge.tsx
    │       └── __tests__/
    │           ├── getHealth.test.ts
    │           ├── useHealth.test.tsx
    │           ├── useHealthSocket.test.tsx
    │           └── HealthStatusCard.test.tsx
    ├── shared/                     # infraestrutura técnica, sem regra de negócio
    │   ├── ui/                     # design system: Button, Card, StatusDot… (+ testes)
    │   │   └── index.ts
    │   ├── api/                    # cliente HTTP tipado
    │   │   ├── openapi.json        # baixado da API (pnpm openapi) — versionado
    │   │   ├── schema.d.ts         # GERADO por openapi-typescript — não editar
    │   │   ├── createApiClient.ts
    │   │   ├── useApiClient.ts
    │   │   ├── errors.ts
    │   │   └── index.ts
    │   ├── ws/                     # cliente WebSocket (reconexão, heartbeat)
    │   │   ├── createWsClient.ts
    │   │   ├── buildWsUrl.ts
    │   │   ├── types.ts
    │   │   └── index.ts
    │   ├── config/
    │   │   ├── runtimeConfig.ts    # server-only: lê API_URL / WS_URL
    │   │   ├── ConfigProvider.tsx  # entrega a config ao código do navegador
    │   │   └── types.ts
    │   ├── providers/
    │   │   └── Providers.tsx       # ConfigProvider + QueryClientProvider
    │   └── types/
    │       └── scope.ts            # Scope = 'public' | 'admin' (do OpenAPI)
    └── test/
        ├── setup.ts                # jest-dom + MSW
        ├── server.ts
        ├── renderWithProviders.tsx
        ├── factories/health.ts
        └── mocks/handlers.ts
```

## Onde colocar código novo

| Situação | Onde fica |
|----------|-----------|
| Nova tela | `src/app/(web)/<rota>/page.tsx` ou `src/app/admin/<rota>/page.tsx` — só compõe |
| Feature usada **só** por uma área | `src/areas/<web\|admin>/features/<nome>/` |
| Feature usada pelas **duas** áreas | `src/features/<nome>/` |
| Componente visual genérico | `src/shared/ui/` |
| Código técnico (HTTP, WS, config, utils sem negócio) | `src/shared/` |
| Na dúvida | Começa na área; sobe para `features/` quando a outra área realmente precisar |

## Arquivos gerados

| Arquivo | Gerado por | Versionado? |
|---------|-----------|-------------|
| `src/shared/api/openapi.json` | `pnpm openapi` (baixa da API) | ✅ (o diff mostra mudanças de contrato) |
| `src/shared/api/schema.d.ts` | `pnpm openapi` (openapi-typescript) | ✅ |
| `.next/`, `node_modules/`, `coverage/`, `playwright-report/` | build/ferramentas | ❌ |
