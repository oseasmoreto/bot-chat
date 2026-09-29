# ADR-0006 — Next.js em modo static export (SPA)

- **Status:** Aceito
- **Data:** 2026-09-29
- **Ticket:** CPBS-275

## Contexto
Os frontends devem ser SPA servidos pelo Nginx dentro da imagem única, sem servidor Node em produção.

## Decisão
`output: 'export'` + `trailingSlash: true` + `images.unoptimized: true`. Admin com `basePath: '/admin'`. Dados buscados no cliente (TanStack Query).

## Alternativas consideradas
- **Next.js com servidor (SSR):** adicionaria um terceiro processo Node na imagem e mais complexidade, sem necessidade de SEO/SSR no momento.
- **Vite + React Router:** SPA mais "pura", mas a stack definida é Next.js.

## Consequências
- Indisponíveis: route handlers, server actions, middleware, SSR/ISR, rewrites/headers do Next, rotas dinâmicas sem `generateStaticParams` (lista completa em [frontend-comum/01-nextjs-static-export.md](../frontend-comum/01-nextjs-static-export.md)).
- Regras de rota/headers ficam no Nginx.
- Variáveis `NEXT_PUBLIC_*` são fixadas no build.
