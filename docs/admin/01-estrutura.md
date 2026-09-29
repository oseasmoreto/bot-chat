# Admin — Estrutura de pastas

> Localização no repositório: `admin/`. Regras de organização em [feature-based](../frontend-comum/02-arquitetura-feature-based.md).

```text
admin/
├── package.json                  # name: "admin"
├── next.config.ts                # output: 'export', basePath: '/admin', trailingSlash: true
├── tsconfig.json                 # extends @bot-varejo/config/tsconfig
├── eslint.config.mjs             # extends @bot-varejo/config/eslint (+ regras de fronteira)
├── postcss.config.mjs
├── vitest.config.ts
├── playwright.config.ts
├── public/                       # assets estáticos (favicon, imagens)
├── src/
│   ├── app/                      # ROTAS — apenas compõem features, sem lógica
│   │   ├── layout.tsx            # layout raiz + Providers
│   │   ├── page.tsx              # "/" (admin: /admin/)
│   │   ├── not-found.tsx
│   │   ├── globals.css           # importa tema do @bot-varejo/config/tailwind
│   │   └── health/
│   │       ├── page.tsx          # "/health/" — tela de status
│   │       └── page.test.tsx     # teste da tela
│   ├── features/                 # FEATURES — cada pasta é isolada
│   │   └── health/
│   │       ├── index.ts          # API pública da feature (único ponto de import externo)
│   │       ├── api/
│   │       │   └── getHealth.ts          # chamada HTTP via api-client
│   │       ├── hooks/
│   │       │   ├── useHealth.ts          # TanStack Query (HTTP)
│   │       │   └── useHealthSocket.ts    # WebSocket (ping/pong)
│   │       ├── components/
│   │       │   ├── HealthStatusCard.tsx
│   │       │   └── HealthStatusBadge.tsx
│   │       ├── types.ts
│   │       └── __tests__/
│   │           ├── HealthStatusCard.test.tsx
│   │           ├── useHealth.test.tsx
│   │           └── useHealthSocket.test.tsx
│   ├── shared/                   # compartilhado DENTRO deste app (não entre apps)
│   │   ├── providers/
│   │   │   └── Providers.tsx     # QueryClientProvider etc.
│   │   ├── layout/
│   │   │   └── AppShell.tsx
│   │   └── config/
│   │       └── env.ts            # leitura tipada de configs
│   └── test/
│       ├── setup.ts              # jest-dom, MSW server (listen/reset/close)
│       ├── server.ts             # setupServer(...handlers)
│       ├── renderWithProviders.tsx # render com QueryClient novo por teste
│       ├── factories/health.ts   # buildHealth({...}) — dados de teste tipados
│       └── mocks/handlers.ts     # handlers MSW padrão (ex.: /api/v1/admin/health)
└── e2e/
    └── health.spec.ts            # Playwright contra o stack via Nginx
```
