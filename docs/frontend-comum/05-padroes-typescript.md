# Frontend comum — Padrões de código TypeScript/React

> Padrões transversais em [06 — Padrões gerais](../06-padroes-gerais.md).

## Nomenclatura

| Elemento | Convenção | Exemplo |
|----------|-----------|---------|
| Função, método, variável | camelCase | `getHealth`, `buildWsUrl`, `retryCount` |
| Componente React | PascalCase | `HealthStatusCard` |
| Hook | `use` + PascalCase | `useHealth`, `useHealthSocket` |
| Tipo, interface, enum | PascalCase | `HealthResponse`, `WsMessage` |
| Constante de módulo | UPPER_SNAKE_CASE | `PING_INTERVAL_MS`, `HEALTH_QUERY_KEY` |
| Booleano | prefixo `is/has/should/can` | `isLoading`, `hasError` |
| Handler de evento (dentro do componente) | `handle` + Evento | `handleSubmit` |
| Prop de callback | `on` + Evento | `onSubmit` |
| Arquivo de componente | PascalCase `.tsx` | `HealthStatusCard.tsx` |
| Arquivo de hook / função | camelCase `.ts` | `useHealth.ts`, `getHealth.ts` |
| Pasta de feature / rota | kebab-case | `features/flow-builder/`, `app/partner-services/` |
| Pacote | `@bot-varejo/<kebab>` | `@bot-varejo/api-client` |
| Teste | `<Arquivo>.test.ts(x)` / `<fluxo>.spec.ts` | `useHealth.test.tsx` |

## Tipagem

- `"strict": true` + `noUncheckedIndexedAccess` + `exactOptionalPropertyTypes`
- Retorno explícito em funções exportadas
- Tipos de API derivados do OpenAPI (nunca à mão)
- `as const` para constantes/literais
- `any` proibido; use `unknown` + *narrowing*
- `@ts-expect-error` com comentário; `@ts-ignore` proibido

## Boas práticas

- **Named exports**; `export default` só onde o Next exige (`page.tsx`, `layout.tsx`, `not-found.tsx`).
- Componentes como `const Nome = (...) => {}`; `'use client'` apenas onde há estado/efeito.
- Estado de servidor com TanStack Query; estado local com `useState`; nada de store global sem ADR.
- Acessibilidade: elementos semânticos, `label` em inputs, foco visível.
- Tailwind: utilitários no JSX; repetição vira componente em `packages/ui`.

## Ordem de imports (TS)

```ts
// 1. libs externas
import { useQuery } from '@tanstack/react-query';

// 2. pacotes do workspace
import { apiClient } from '@bot-varejo/api-client';

// 3. alias do app
import { Providers } from '@/shared/providers/Providers';

// 4. relativos
import { getHealth } from '../api/getHealth';
```

Python: ordenado pelo ruff (`I`) — stdlib, terceiros, `bot_varejo`.
