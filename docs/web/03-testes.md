# Web (public) — Testes

> Estratégia geral em [05 — Estratégia de testes](../05-estrategia-testes.md); infraestrutura de testes comum em [frontend-comum](../frontend-comum/06-testes.md).

## Componente de feature com MSW

```tsx
// web/src/features/health/__tests__/HealthStatusCard.test.tsx
import { screen } from '@testing-library/react';
import { http, HttpResponse } from 'msw';
import { describe, expect, it, vi } from 'vitest';

import { buildHealth } from '@/test/factories/health';
import { renderWithProviders } from '@/test/renderWithProviders';
import { server } from '@/test/server';

import { HealthStatusCard } from '../components/HealthStatusCard';

vi.mock('../hooks/useHealthSocket', () => ({
  useHealthSocket: () => ({ status: 'connecting' }),
}));

describe('HealthStatusCard', () => {
  it('exibe status ok quando a API responde saudável', async () => {
    server.use(
      http.get('*/api/v1/public/health', () => HttpResponse.json(buildHealth({ status: 'ok' }))),
    );

    renderWithProviders(<HealthStatusCard />);

    expect(await screen.findByTestId('http-status')).toHaveTextContent('ok');
  });

  it('exibe indisponível quando a API falha', async () => {
    server.use(http.get('*/api/v1/public/health', () => HttpResponse.error()));

    renderWithProviders(<HealthStatusCard />);

    expect(await screen.findByTestId('http-status')).toHaveTextContent('indisponível');
  });
});
```

## Tela (rota)

```tsx
// web/src/app/health/page.test.tsx
import { screen } from '@testing-library/react';
import { expect, it } from 'vitest';

import { renderWithProviders } from '@/test/renderWithProviders';

import HealthPage from './page';

it('renderiza o card de status da plataforma', () => {
  renderWithProviders(<HealthPage />);

  expect(screen.getByText('Status da plataforma')).toBeInTheDocument();
});
```

## E2E (Playwright contra o container)

```ts
// web/e2e/health.spec.ts
import { expect, test } from '@playwright/test';

test('web mostra a API saudável via HTTP e WebSocket', async ({ page }) => {
  await page.goto('/health/');

  await expect(page.getByTestId('http-status')).toContainText('ok');
  await expect(page.getByTestId('ws-status')).toContainText('ms');
});
```

`playwright.config.ts` usa `baseURL: process.env.E2E_BASE_URL ?? 'http://localhost:8080'`.
