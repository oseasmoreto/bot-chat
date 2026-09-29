# Web (public) — Feature `health` (código de referência)

Tela de status do escopo **public**: consome `GET /api/v1/public/health` (HTTP) e `health.ping`/`health.pong` em `/ws/public` (WebSocket).

## `features/health/types.ts`

```ts
import type { components } from '@bot-varejo/api-client';

export type HealthResponse = components['schemas']['HealthResponse'];
export type HealthStatus = HealthResponse['status'];
```

## `features/health/api/getHealth.ts`

```ts
import { apiClient, ApiError } from '@bot-varejo/api-client';

import type { HealthResponse } from '../types';

export const getHealth = async (): Promise<HealthResponse> => {
  const { data, error, response } = await apiClient.GET('/api/v1/public/health');
  if (data) return data;
  // 503 = backend respondeu, mas com status "down": ainda é um relatório válido.
  if (response.status === 503 && error) return error;
  throw new ApiError(response.status, error);
};
```

> No `admin/`, a única diferença é o path: `/api/v1/admin/health`.

## `features/health/hooks/useHealth.ts`

```ts
import { useQuery } from '@tanstack/react-query';

import { getHealth } from '../api/getHealth';

export const HEALTH_QUERY_KEY = ['health'] as const;
const REFETCH_INTERVAL_MS = 30_000;

export const useHealth = () =>
  useQuery({
    queryKey: HEALTH_QUERY_KEY,
    queryFn: getHealth,
    refetchInterval: REFETCH_INTERVAL_MS,
  });
```

## `features/health/hooks/useHealthSocket.ts`

```ts
import { useEffect, useState } from 'react';

import { buildWsUrl, createWsClient, type WsMessage } from '@bot-varejo/ws-client';

import type { HealthResponse } from '../types';

const PING_INTERVAL_MS = 15_000;

export type SocketState =
  | { status: 'connecting' }
  | { status: 'open'; lastPong: HealthResponse; latencyMs: number }
  | { status: 'closed' };

export const useHealthSocket = (): SocketState => {
  const [state, setState] = useState<SocketState>({ status: 'connecting' });

  useEffect(() => {
    const client = createWsClient({ url: buildWsUrl('public') });
    const sentAt = new Map<string, number>();

    const sendPing = () => {
      const id = crypto.randomUUID();
      sentAt.set(id, performance.now());
      client.send({ type: 'health.ping', id, payload: {} });
    };

    const unsubscribe = client.subscribe((message: WsMessage) => {
      if (message.type !== 'health.pong' || !message.id) return;
      const startedAt = sentAt.get(message.id);
      sentAt.delete(message.id);
      setState({
        status: 'open',
        lastPong: message.payload as HealthResponse,
        latencyMs: startedAt ? Math.round(performance.now() - startedAt) : 0,
      });
    });

    client.onStatusChange((status) => {
      if (status === 'open') sendPing();
      if (status === 'closed') setState({ status: 'closed' });
    });
    const timer = setInterval(sendPing, PING_INTERVAL_MS);

    return () => {
      clearInterval(timer);
      unsubscribe();
      client.close();
    };
  }, []);

  return state;
};
```

## `features/health/components/HealthStatusCard.tsx`

```tsx
'use client';

import { Card, StatusDot } from '@bot-varejo/ui';

import { useHealth } from '../hooks/useHealth';
import { useHealthSocket } from '../hooks/useHealthSocket';

export const HealthStatusCard = () => {
  const http = useHealth();
  const socket = useHealthSocket();

  return (
    <Card title="Status da plataforma">
      <dl className="grid grid-cols-2 gap-2 text-sm">
        <dt>API (HTTP)</dt>
        <dd data-testid="http-status">
          <StatusDot status={http.data?.status ?? (http.isError ? 'down' : 'unknown')} />
          {http.data?.status ?? (http.isLoading ? 'verificando…' : 'indisponível')}
        </dd>

        <dt>Tempo real (WebSocket)</dt>
        <dd data-testid="ws-status">
          <StatusDot status={socket.status === 'open' ? socket.lastPong.status : 'unknown'} />
          {socket.status === 'open' ? `${socket.latencyMs} ms` : socket.status}
        </dd>

        <dt>Versão</dt>
        <dd>{http.data?.version ?? '—'}</dd>
      </dl>
    </Card>
  );
};
```

## `features/health/index.ts` — API pública

```ts
export { HealthStatusCard } from './components/HealthStatusCard';
export { useHealth, HEALTH_QUERY_KEY } from './hooks/useHealth';
export type { HealthResponse, HealthStatus } from './types';
```

## `app/health/page.tsx` — rota fina

```tsx
import { HealthStatusCard } from '@/features/health';

export default function HealthPage() {
  return (
    <main className="mx-auto max-w-2xl p-6">
      <HealthStatusCard />
    </main>
  );
}
```

## `shared/providers/Providers.tsx`

```tsx
'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useState, type ReactNode } from 'react';

export const Providers = ({ children }: { children: ReactNode }) => {
  const [queryClient] = useState(() => new QueryClient());
  return <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>;
};
```
