# Frontend comum — Testes

Infraestrutura de testes **igual nos dois apps**. Exemplos específicos: [web](../web/03-testes.md) · [admin](../admin/03-testes.md). Estratégia geral: [05 — Estratégia de testes](../05-estrategia-testes.md).

## Ferramentas

| Ferramenta | Uso |
|------------|-----|
| Vitest (ambiente `jsdom`) | Runner de testes unitários e de componente |
| Testing Library + `jest-dom` | Render e asserções orientadas ao usuário |
| MSW | Intercepta HTTP — os testes exercitam o `api-client` real |
| Playwright | E2E contra o container (Nginx → builds + API) |

## Convenções

| Item | Regra |
|------|-------|
| Local | `__tests__/` ao lado do código da feature; teste de tela ao lado da `page.tsx`; E2E em `<app>/e2e/` |
| Nome | `<Arquivo>.test.ts(x)`; E2E `<fluxo>.spec.ts` |
| Descrição | `it('exibe … quando …')` em pt-BR |
| Estrutura | Arrange / Act / Assert separados por linha em branco |
| Dublês | MSW para HTTP; `vi.mock` apenas para isolar o hook de WebSocket |
| Seletores | Por papel/texto acessível (`getByRole`, `getByText`); `data-testid` só sem alternativa |
| Dados | Factories tipadas em `src/test/factories/` |
| Cobertura | ≥ 80% linhas e branches |

## `vitest.config.ts`

```ts
import react from '@vitejs/plugin-react';
import tsconfigPaths from 'vite-tsconfig-paths';
import { defineConfig } from 'vitest/config';

export default defineConfig({
  plugins: [react(), tsconfigPaths()],
  test: {
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
    exclude: ['e2e/**', 'node_modules/**'],
    coverage: { provider: 'v8', thresholds: { lines: 80, branches: 80 } },
  },
});
```

## `src/test/setup.ts`

```ts
import '@testing-library/jest-dom/vitest';
import { afterAll, afterEach, beforeAll } from 'vitest';

import { server } from './server';

beforeAll(() => server.listen({ onUnhandledRequest: 'error' }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

> `onUnhandledRequest: 'error'` faz o teste falhar se algum código chamar uma API não mockada.

## `src/test/server.ts`

```ts
import { setupServer } from 'msw/node';

import { handlers } from './mocks/handlers';

export const server = setupServer(...handlers);
```

## `src/test/renderWithProviders.tsx`

```tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { render, type RenderOptions } from '@testing-library/react';
import type { ReactElement } from 'react';

// QueryClient novo por teste: sem cache vazando entre testes, sem retry mascarando erro.
export const renderWithProviders = (ui: ReactElement, options?: RenderOptions) => {
  const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return render(<QueryClientProvider client={queryClient}>{ui}</QueryClientProvider>, options);
};
```

## `src/test/factories/health.ts`

```ts
import type { HealthResponse } from '@/features/health';

export const buildHealth = (overrides: Partial<HealthResponse> = {}): HealthResponse => ({
  status: 'ok',
  scope: 'admin', // no web: 'public'
  version: 'test',
  uptimeSeconds: 1,
  checkedAt: '2026-01-01T00:00:00Z',
  components: [],
  ...overrides,
});
```

## `playwright.config.ts`

```ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  use: { baseURL: process.env.E2E_BASE_URL ?? 'http://localhost:8080' },
});
```

Os E2E rodam **contra o `docker compose up`** (Nginx real), nunca contra o `next dev` isolado — assim validam roteamento, `/api` e `/ws` de verdade.
