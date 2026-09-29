# 03 — Next.js padrão usado como SPA

Rodamos o **Next.js padrão** (servidor Node, `output: 'standalone'`) e o usamos como **SPA**: o servidor entrega a "casca" das telas e o navegador faz todo o resto — interação, navegação e busca de dados direto na API ([ADR-0001](./adr/0001-nextjs-padrao-como-spa.md)).

## 1. Quem faz o quê

| Responsabilidade | Onde | Como |
|------------------|------|------|
| HTML inicial das telas | Servidor Next | `page.tsx`/`layout.tsx` (Server Components finos, sem fetch) |
| Configuração de runtime (URL da API) | Servidor Next | Layout raiz lê `process.env` e passa para o `ConfigProvider` |
| Headers de segurança | Servidor Next | `headers()` no `next.config.ts` |
| Liveness do container | Servidor Next | Route handler `GET /healthz` |
| Proteção do `/admin` (futuro) | Servidor Next | `middleware.ts` redirecionando para login |
| Interação e estado da tela | Navegador | Client Components (`'use client'`) nas features |
| **Busca de dados** | **Navegador** | TanStack Query + `apiClient` → `https://api.<dominio>` |
| Tempo real | Navegador | WebSocket direto na API |
| Navegação entre telas | Navegador | `next/link` / `useRouter` (sem recarregar a página) |

## 2. Regras do modo SPA

| # | Regra | Por quê |
|---|-------|---------|
| 1 | **Nenhum fetch de dados de negócio no servidor** (Server Components, Server Actions, Route Handlers) | O servidor Next não é backend: a API é o FastAPI. Evita dois backends e duplicação de regras |
| 2 | Toda busca de dados usa **TanStack Query** no navegador via `useApiClient()` | Cache, retry, loading/erro padronizados |
| 3 | `page.tsx` e `layout.tsx` são **finos**: só compõem componentes de áreas/features | Teste e lógica ficam nas features |
| 4 | Componentes com estado, efeitos ou hooks de dados levam `'use client'` e ficam em `features/`/`areas/` | Fronteira servidor/cliente explícita |
| 5 | **Server Actions proibidas**; Route Handlers só para infraestrutura (`/healthz`) | Mesmo motivo da regra 1 |
| 6 | Nada de segredo em código do navegador. Variáveis `NEXT_PUBLIC_*` **não são usadas** | Config vem em runtime pelo `ConfigProvider`; segredos ficam no backend |
| 7 | Rotas dinâmicas são permitidas (`/admin/flows/[flowId]`) — o parâmetro é lido no cliente e os dados vêm da API | O servidor padrão renderiza qualquer rota sob demanda |

## 3. `next.config.ts`

```ts
import type { NextConfig } from 'next';

const securityHeaders = [
  { key: 'X-Content-Type-Options', value: 'nosniff' },
  { key: 'X-Frame-Options', value: 'DENY' },
  { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
  { key: 'Permissions-Policy', value: 'camera=(), microphone=(), geolocation=()' },
];

const nextConfig: NextConfig = {
  output: 'standalone',      // gera .next/standalone/server.js para a imagem Docker
  reactStrictMode: true,
  poweredByHeader: false,
  async headers() {
    return [{ source: '/:path*', headers: securityHeaders }];
  },
};

export default nextConfig;
```

> **Content-Security-Policy** será adicionada quando os domínios estiverem definidos (precisa de `connect-src` com `https://api.<dominio>` e `wss://api.<dominio>`).

## 4. Layout raiz — configuração em runtime

```tsx
// src/app/layout.tsx
import { connection } from 'next/server';
import type { ReactNode } from 'react';

import { getRuntimeConfig } from '@/shared/config/runtimeConfig';
import { Providers } from '@/shared/providers/Providers';

import './globals.css';

export default async function RootLayout({ children }: { children: ReactNode }) {
  await connection(); // renderiza por requisição: lê o env do CONTAINER, não do build
  const config = getRuntimeConfig();

  return (
    <html lang="pt-BR">
      <body>
        <Providers config={config}>{children}</Providers>
      </body>
    </html>
  );
}
```

Detalhes de `getRuntimeConfig` e `ConfigProvider` em [07 — Integração com a API](./07-integracao-api.md).

## 5. `GET /healthz` — liveness do servidor

```ts
// src/app/healthz/route.ts
export const dynamic = 'force-dynamic';

export const GET = (): Response => Response.json({ status: 'ok' });
```

Usado pelo HEALTHCHECK da imagem. Indica que **o servidor do front** está de pé — não consulta a API (o status da API é mostrado nas telas `/health` e `/admin/health`).
