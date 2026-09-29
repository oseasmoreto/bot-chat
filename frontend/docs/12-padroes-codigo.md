# 12 — Padrões de código

## Nomenclatura: camelCase

A orientação da task é **camelCase para métodos**: no TypeScript é o padrão da linguagem e vale para funções, métodos e variáveis. O contrato da API também é camelCase (o backend converte do Python), então os tipos gerados já chegam em camelCase ([ADR-0006](./adr/0006-convencao-de-nomes.md)).


## Tabela de nomenclatura

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
| Pasta de feature / rota | kebab-case | `features/flow-builder/`, `app/admin/partner-services/` |
| Área | nome curto, minúsculo | `areas/web/`, `areas/admin/` |
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
- Modo SPA: nada de fetch em Server Components, Server Actions ou Route Handlers de negócio ([03](./03-nextjs-spa.md)).
- Acessibilidade: elementos semânticos, `label` em inputs, foco visível.
- Tailwind: utilitários no JSX; repetição vira componente em `src/shared/ui`.

## Ordem de imports (TS)

```ts
// 1. libs externas
import { useQuery } from '@tanstack/react-query';

// 2. alias do projeto (shared → features → areas)
import { useApiClient } from '@/shared/api';

// 3. relativos (dentro da própria feature)
import { getHealth } from '../api/getHealth';
```

Python: ordenado pelo ruff (`I`) — stdlib, terceiros, `bot_varejo`.


## Boas práticas gerais

- **Funções pequenas** com uma responsabilidade; se precisa de "e" para descrever, divida.
- **Early return** em vez de `if` aninhado.
- **Sem números/strings mágicos**: constantes nomeadas.
- **Imutabilidade por padrão** (`frozen=True`, `readonly`, `as const`).
- **Comentários explicam o porquê**, não o quê. Código auto-explicativo dispensa comentário.
- **Sem código morto** nem comentado — o git guarda o histórico.
- **Sem segredos no código** — variáveis de ambiente; `.env` nunca é commitado.
- Textos da interface em **pt-BR**; código (nomes) em **inglês**.

## Formatação e lint

| Ferramenta | Config |
|------------|--------|
| Prettier | `singleQuote: true`, `semi: true`, `trailingComma: 'all'`, `printWidth: 100` |
| ESLint | typescript-eslint (strict), react-hooks, jsx-a11y, `@next/eslint-plugin-next`, **boundaries** ([04](./04-organizacao-areas-features.md#5-fronteiras-garantidas-por-lint)), ordem de imports |
| TypeScript | `tsc --noEmit` com `strict` ([09](./09-estilo-e-typescript.md)) |
| EditorConfig | UTF-8, LF, indentação 2, newline final |
| pre-commit | roda prettier e eslint nos arquivos alterados de `frontend/` |
