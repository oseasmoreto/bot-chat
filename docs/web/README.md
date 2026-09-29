# Web (escopo public)

**Pasta no repositório:** `web/`  ·  **Escopo:** `public`  ·  **Servido em:** `/`

Frontend usado pelo **cliente final** do parceiro de varejo: onde, no futuro, ele conversará com o bot para contratar e consultar serviços.

> Stack, arquitetura feature-based, pacotes compartilhados e padrões são **comuns aos dois fronts** e estão em [frontend-comum](../frontend-comum/README.md). Aqui fica só o que é específico do web.

## Documentos

| # | Documento | Conteúdo |
|---|-----------|----------|
| 01 | [Estrutura de pastas](./01-estrutura.md) | Árvore de `web/` |
| 02 | [Feature `health`](./02-feature-health.md) | Código de referência da tela de status |
| 03 | [Testes](./03-testes.md) | Exemplos de teste de feature, tela e E2E |

## Configuração específica

```ts
// web/next.config.ts
import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  output: 'export',
  trailingSlash: true,
  images: { unoptimized: true },
  transpilePackages: ['@bot-varejo/ui', '@bot-varejo/api-client', '@bot-varejo/ws-client'],
};

export default nextConfig;
```

| Item | Valor |
|------|-------|
| `package.json` → `name` | `web` |
| `basePath` | nenhum (raiz) |
| Saída do build | `web/out/` → copiado para `/var/www/html/` na imagem |
| Porta do `next dev` | `3000` (acessado via Nginx em `http://localhost:8080/`) |
| API consumida | `/api/v1/public/*` |
| WebSocket | `/ws/public` |
| Pacotes do workspace | `@bot-varejo/ui`, `api-client`, `ws-client`, `config` via `workspace:*` — ver [como os apps consomem os pacotes](../frontend-comum/03-pacotes-compartilhados.md#como-web-e-admin-consomem-os-pacotes) |

## Telas (rotas)

| Rota | Arquivo | Feature | Descrição |
|------|---------|---------|-----------|
| `/` | `src/app/page.tsx` | — | Página inicial (placeholder nesta fase, com link para status) |
| `/health/` | `src/app/health/page.tsx` | `health` | Status da API via HTTP e WebSocket |
| qualquer outra | `src/app/not-found.tsx` | — | Página 404 do web (servida pelo Nginx como `/404.html`) |

## Features

| Feature | Pasta | Status | Descrição |
|---------|-------|--------|-----------|
| `health` | `src/features/health/` | CPBS-275 | Tela de status: `GET /api/v1/public/health` + `health.ping` no WS |
| `chat` | `src/features/chat/` | futuro | Conversa com o bot em tempo real (WebSocket) |

## Comandos

| Ação | Comando (na raiz do repo) |
|------|---------------------------|
| Dev (hot reload, via Nginx) | `make dev` → `http://localhost:8080/` |
| Dev isolado | `pnpm --filter web dev` (porta 3000; `/api` e `/ws` não funcionam sem o Nginx) |
| Build | `pnpm --filter web build` |
| Testes | `pnpm --filter web test` |
| E2E | `pnpm --filter web e2e` (com `make up` rodando) |
| Lint / tipos | `pnpm --filter web lint` · `pnpm --filter web typecheck` |

## Pontos de atenção

- O build do web ocupa a raiz de `/var/www/html/`, e o admin fica em `/var/www/html/admin/`: **o web nunca pode ter uma rota `/admin`**.
- Todo conteúdo aqui é **público** — nunca exibir dados de operação/admin.
- Nesta fase o web só mostra o status; o chat vem em tasks futuras.
