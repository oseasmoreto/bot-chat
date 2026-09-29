# Frontend comum — Next.js em modo static export

O Nginx serve arquivos prontos; não existe servidor Node em produção ([ADR-0006](../adr/0006-nextjs-static-export.md)). Consequências que **todo dev precisa conhecer**:

| Não disponível no static export | Alternativa |
|---------------------------------|-------------|
| Route Handlers (`app/api/*`) e Server Actions | Toda API é o backend FastAPI (`/api/*`) |
| `middleware.ts` | Regras de rota no Nginx ou guards client-side |
| SSR por requisição, ISR, `cookies()`/`headers()` | Busca de dados no cliente (TanStack Query) |
| Rotas dinâmicas sem `generateStaticParams` | Usar query string (`/flows/?id=123`) ou gerar params no build |
| Otimização do `next/image` | `images.unoptimized: true` |
| `rewrites`/`redirects`/`headers` do `next.config` | Configurar no Nginx |

## `next.config.ts`

```ts
// admin/next.config.ts
import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  output: 'export',
  basePath: '/admin',          // web/: remover esta linha
  trailingSlash: true,         // gera /health/index.html → casa com try_files do Nginx
  images: { unoptimized: true },
  transpilePackages: ['@bot-varejo/ui', '@bot-varejo/api-client', '@bot-varejo/ws-client'],
};

export default nextConfig;
```

> O build gera `admin/out/`. Na imagem, `web/out/` vai para `/var/www/html/` e `admin/out/` para `/var/www/html/admin/`. Por isso **o app `web` nunca pode ter uma rota `/admin`**.
