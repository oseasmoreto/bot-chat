# 06 — Área admin (escopo admin)

**URL:** `/admin` · **Rotas:** `src/app/admin/` · **Código exclusivo:** `src/areas/admin/` · **Escopo da API:** `admin`

Área usada por **operadores, time interno e parceiros**: onde, no futuro, serão construídos fluxos de conversa, configuradas integrações e acompanhados os atendimentos.

## Telas (rotas)

| Rota | Arquivo | Compõe | Descrição |
|------|---------|--------|-----------|
| `/admin` | `src/app/admin/page.tsx` | `AdminShell` | Início do admin (placeholder, com link para o status) |
| `/admin/health` | `src/app/admin/health/page.tsx` | `HealthStatusCard scope="admin"` | Status da API (escopo admin) via HTTP e WebSocket |

## Layout da área

```tsx
// src/app/admin/layout.tsx
import type { ReactNode } from 'react';

import { AdminShell } from '@/areas/admin/layout/AdminShell';

export default function AdminLayout({ children }: { children: ReactNode }) {
  return <AdminShell>{children}</AdminShell>;
}
```

`AdminShell` (menu lateral, cabeçalho de operação) vive em `src/areas/admin/layout/` e tem teste próprio.

## Features

| Feature | Local | Status | Descrição |
|---------|-------|--------|-----------|
| `health` | `src/features/health/` (comum) | atual | `GET /api/v1/admin/health` + `health.ping` em `/api/v1/ws/admin` |
| `flows` | `src/areas/admin/features/flows/` | futuro | Construtor de fluxos de conversa |
| `integrations` | `src/areas/admin/features/integrations/` | futuro | Integrações com parceiros |
| `partners` | `src/areas/admin/features/partners/` | futuro | Cadastro de parceiros e serviços |

## Pontos de atenção

- **Ainda não há autenticação**: `/admin` e `/api/v1/admin/*` estão abertos. Proteger é pré-requisito antes de qualquer dado real. Plano: `middleware.ts` no front redirecionando `/admin/*` para login + autorização por escopo na API.
- O JavaScript do admin só é baixado ao acessar `/admin`, mas **não é secreto** — segurança é responsabilidade da API.
- A área admin **não importa nada** de `src/areas/web/` (lint bloqueia).
