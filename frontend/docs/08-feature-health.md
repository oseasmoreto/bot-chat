# 08 — Feature `health` (código de referência)

Feature **comum às duas áreas** (`src/features/health/`), parametrizada pelo escopo: a área web a usa com `scope="public"` e a área admin com `scope="admin"`. Mostra o status da API via HTTP (`GET /api/v1/{scope}/health`) e via WebSocket (`health.ping` → `health.pong` em `/api/v1/ws/{scope}`).

## `types.ts`

```ts
import type { components } from '@/shared/api/schema';

export type HealthResponse = components['schemas']['HealthResponse'];
export type HealthStatus = HealthResponse['status'];
```

## `api/getHealth.ts`

```ts
import { ApiError, type ApiClient } from '@/shared/api';
import type { Scope } from '@/shared/types/scope';

import type { HealthResponse } from '../types';

export const getHealth = async (client: ApiClient, scope: Scope): Promise<HealthResponse> => {
  const { data, error, response } =
    scope === 'public'
      ? await client.GET('/api/v1/public/health')
      : await client.GET('/api/v1/admin/health');

  if (data) return data;
  // 503 = API respondeu com status "down": ainda é um relatório válido.
  if (response.status === 503 && error) return error;
  throw new ApiError(response.status, error);
};
```

## `hooks/useHealth.ts`

```ts
import { useQuery } from '@tanstack/react-query';

import { useApiClient } from '@/shared/api';
import type { Scope } from '@/shared/types/scope';

import { getHealth } from '../api/getHealth';

export const HEALTH_QUERY_KEY = ['health'] as const;
const REFETCH_INTERVAL_MS = 30_000;

export const useHealth = (scope: Scope) => {
  const apiClient = useApiClient();
  return useQuery({
    queryKey: [...HEALTH_QUERY_KEY, scope],
    queryFn: () => getHealth(apiClient, scope),
    refetchInterval: REFETCH_INTERVAL_MS,
  });
};
```

## `hooks/useHealthSocket.ts`

```ts
import { useEffect, useState } from 'react';

import { useRuntimeConfig } from '@/shared/config/ConfigProvider';
import type { Scope } from '@/shared/types/scope';
import { buildWsUrl, createWsClient, type WsMessage } from '@/shared/ws';

import type { HealthResponse } from '../types';

const PING_INTERVAL_MS = 15_000;

export type SocketState =
  | { status: 'connecting' }
  | { status: 'open'; lastPong: HealthResponse; latencyMs: number }
  | { status: 'closed' };

export const useHealthSocket = (scope: Scope): SocketState => {
  const { wsUrl } = useRuntimeConfig();
  const [state, setState] = useState<SocketState>({ status: 'connecting' });

  useEffect(() => {
    const client = createWsClient({ url: buildWsUrl(wsUrl, scope) });
    const sentAt = new Map<string, number>();

    const sendPing = () => {
      const id = crypto.randomUUID();
      sentAt.set(id, performance.now());
      client.send({ type: 'health.ping', id, payload: {} });
    };

    const unsubscribeMessages = client.subscribe((message: WsMessage) => {
      if (message.type !== 'health.pong' || !message.id) return;
      const startedAt = sentAt.get(message.id);
      sentAt.delete(message.id);
      setState({
        status: 'open',
        lastPong: message.payload as HealthResponse,
        latencyMs: startedAt ? Math.round(performance.now() - startedAt) : 0,
      });
    });

    const unsubscribeStatus = client.onStatusChange((status) => {
      if (status === 'open') sendPing();
      if (status === 'closed') setState({ status: 'closed' });
    });
    const timer = setInterval(sendPing, PING_INTERVAL_MS);

    return () => {
      clearInterval(timer);
      unsubscribeMessages();
      unsubscribeStatus();
      client.close();
    };
  }, [wsUrl, scope]);

  return state;
};
```

## `components/HealthStatusCard.tsx`

```tsx
'use client';

import type { Scope } from '@/shared/types/scope';
import { Card, StatusDot } from '@/shared/ui';

import { useHealth } from '../hooks/useHealth';
import { useHealthSocket } from '../hooks/useHealthSocket';

export const HealthStatusCard = ({ scope }: { scope: Scope }) => {
  const http = useHealth(scope);
  const socket = useHealthSocket(scope);

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

        <dt>Escopo</dt>
        <dd>{http.data?.scope ?? scope}</dd>

        <dt>Versão da API</dt>
        <dd>{http.data?.version ?? '—'}</dd>
      </dl>
    </Card>
  );
};
```

## `index.ts` — API pública

```ts
export { HealthStatusCard } from './components/HealthStatusCard';
export { useHealth, HEALTH_QUERY_KEY } from './hooks/useHealth';
export type { HealthResponse, HealthStatus } from './types';
```

## Uso nas rotas

```tsx
// src/app/(web)/health/page.tsx
import { HealthStatusCard } from '@/features/health';

export default function WebHealthPage() {
  return (
    <main className="mx-auto max-w-2xl p-6">
      <HealthStatusCard scope="public" />
    </main>
  );
}
```

```tsx
// src/app/admin/health/page.tsx
import { HealthStatusCard } from '@/features/health';

export default function AdminHealthPage() {
  return (
    <main className="p-6">
      <HealthStatusCard scope="admin" />
    </main>
  );
}
```
