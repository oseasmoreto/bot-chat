# 05 — Área web (escopo public)

**URL:** `/` · **Rotas:** `src/app/(web)/` · **Código exclusivo:** `src/areas/web/` · **Escopo da API:** `public`

Área usada pelo **cliente final** do parceiro de varejo: onde, no futuro, ele conversará com o bot para contratar e consultar serviços.

`(web)` é um *route group* do Next: organiza os arquivos sem aparecer na URL. Assim a área web ocupa a raiz (`/`) enquanto a admin fica em `/admin`.

## Telas (rotas)

| Rota | Arquivo | Compõe | Descrição |
|------|---------|--------|-----------|
| `/` | `src/app/(web)/page.tsx` | `WebShell` | Página inicial (placeholder, com link para o status) |
| `/health` | `src/app/(web)/health/page.tsx` | `HealthStatusCard scope="public"` | Status da API (escopo public) via HTTP e WebSocket |
| qualquer outra | `src/app/not-found.tsx` | — | Página 404 |

## Layout da área

```tsx
// src/app/(web)/layout.tsx
import type { ReactNode } from 'react';

import { WebShell } from '@/areas/web/layout/WebShell';

export default function WebLayout({ children }: { children: ReactNode }) {
  return <WebShell>{children}</WebShell>;
}
```

`WebShell` (cabeçalho, rodapé e estilo do público final) vive em `src/areas/web/layout/` e tem teste próprio.

## Features

| Feature | Local | Status | Descrição |
|---------|-------|--------|-----------|
| `health` | `src/features/health/` (comum) | atual | `GET /api/v1/public/health` + `health.ping` em `/api/v1/ws/public` |
| `chat` | `src/areas/web/features/chat/` | futuro | Conversa com o bot em tempo real |

## Pontos de atenção

- Tudo aqui é **público**: nunca exibir dados de operação/admin nem chamar rotas `/api/v1/admin/*`.
- A área web **não importa nada** de `src/areas/admin/` (lint bloqueia).
- Nenhuma rota do web pode começar com `/admin` (conflitaria com a área admin).
