# ADR-0001 — Next.js padrão (servidor Node) usado como SPA

- **Status:** Aceito
- **Data:** 2026-09-29

## Contexto
O frontend roda em imagem `node:24` própria, em domínio próprio (`app.<dominio>`), e precisa ter comportamento de **SPA**, consumindo a API em outro domínio.

## Decisão
- Next.js com servidor padrão, `output: 'standalone'` (`node server.js`).
- Uso como SPA: dados buscados **no navegador** (TanStack Query) direto na API; páginas e layouts finos; navegação client-side.
- Proibido: fetch de dados de negócio no servidor, Server Actions e Route Handlers de negócio. Permitido no servidor: config de runtime, headers, `/healthz` e (futuro) `middleware.ts` de autenticação.

## Alternativas consideradas
- **SSR completo com fetch no servidor:** criaria um segundo "backend" no Node, duplicando responsabilidades da API.

## Consequências
- Mesma imagem em todos os ambientes ([ADR-0004](./0004-config-em-runtime.md)).
- Rotas dinâmicas livres e `middleware.ts` disponível para o `/admin`.
- O time precisa respeitar as regras do modo SPA ([03](../03-nextjs-spa.md)) — revisadas no MR.
