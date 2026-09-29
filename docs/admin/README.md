# Admin (escopo admin)

**Pasta no repositório:** `admin/`  ·  **Escopo:** `admin`  ·  **Servido em:** `/admin/`

Frontend usado por **operadores, time interno e parceiros**: onde, no futuro, serão construídos fluxos de conversa, configuradas integrações e acompanhados os atendimentos.

> Stack, arquitetura feature-based, pacotes compartilhados e padrões são **comuns aos dois fronts** e estão em [frontend-comum](../frontend-comum/README.md). Aqui fica só o que é específico do admin.

## Documentos

| # | Documento | Conteúdo |
|---|-----------|----------|
| 01 | [Estrutura de pastas](./01-estrutura.md) | Árvore de `admin/` |
| 02 | [Feature `health`](./02-feature-health.md) | Código de referência da tela de status |
| 03 | [Testes](./03-testes.md) | Exemplos de teste de feature, tela e E2E |

## Configuração específica

```ts
// admin/next.config.ts
import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  output: 'export',
  basePath: '/admin',
  trailingSlash: true,
  images: { unoptimized: true },
  transpilePackages: ['@bot-varejo/ui', '@bot-varejo/api-client', '@bot-varejo/ws-client'],
};

export default nextConfig;
```

| Item | Valor |
|------|-------|
| `package.json` → `name` | `admin` |
| `basePath` | `/admin` — todos os links e assets saem com o prefixo (`/admin/_next/...`) |
| Saída do build | `admin/out/` → copiado para `/var/www/html/admin/` na imagem |
| Porta do `next dev` | `3001` (acessado via Nginx em `http://localhost:8080/admin/`) |
| API consumida | `/api/v1/admin/*` |
| WebSocket | `/ws/admin` |
| Pacotes do workspace | `@bot-varejo/ui`, `api-client`, `ws-client`, `config` via `workspace:*` — ver [como os apps consomem os pacotes](../frontend-comum/03-pacotes-compartilhados.md#como-web-e-admin-consomem-os-pacotes) |

## Telas (rotas)

| Rota | Arquivo | Feature | Descrição |
|------|---------|---------|-----------|
| `/admin/` | `src/app/page.tsx` | — | Página inicial (placeholder nesta fase, com link para status) |
| `/admin/health/` | `src/app/health/page.tsx` | `health` | Status da API via HTTP e WebSocket |
| qualquer outra | `src/app/not-found.tsx` | — | Página 404 do admin (servida pelo Nginx como `/admin/404.html`) |

## Features

| Feature | Pasta | Status | Descrição |
|---------|-------|--------|-----------|
| `health` | `src/features/health/` | CPBS-275 | Tela de status: `GET /api/v1/admin/health` + `health.ping` no WS |
| `flows` | `src/features/flows/` | futuro | Construtor de fluxos de conversa |
| `integrations` | `src/features/integrations/` | futuro | Configuração de integrações com parceiros |
| `partners` | `src/features/partners/` | futuro | Cadastro de parceiros e serviços |

## Comandos

| Ação | Comando (na raiz do repo) |
|------|---------------------------|
| Dev (hot reload, via Nginx) | `make dev` → `http://localhost:8080/admin/` |
| Dev isolado | `pnpm --filter admin dev` (porta 3001; `/api` e `/ws` não funcionam sem o Nginx) |
| Build | `pnpm --filter admin build` |
| Testes | `pnpm --filter admin test` |
| E2E | `pnpm --filter admin e2e` (com `make up` rodando) |
| Lint / tipos | `pnpm --filter admin lint` · `pnpm --filter admin typecheck` |

## Pontos de atenção

- **Ainda não há autenticação**: nesta fase `/admin` e `/api/v1/admin/*` estão abertos. Proteger é pré-requisito antes de qualquer dado real (context `identity`, futuro).
- Por causa do `basePath`, use sempre `next/link` e caminhos relativos ao app (`/health/`), nunca `/admin/health/` hardcoded — o Next adiciona o prefixo.
- `/admin` (sem barra) é redirecionado pelo Nginx para `/admin/`.
