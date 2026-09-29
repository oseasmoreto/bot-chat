# ADRs — Architecture Decision Records

Cada decisão de arquitetura relevante vira um arquivo `NNNN-titulo.md` com o formato:

```markdown
# ADR-NNNN — Título

- **Status:** Proposto | Aceito | Substituído por ADR-XXXX | Descontinuado
- **Data:** AAAA-MM-DD
- **Ticket:** CPBS-xxx

## Contexto
O problema e as forças envolvidas.

## Decisão
O que foi decidido.

## Alternativas consideradas
O que foi descartado e por quê.

## Consequências
Positivas, negativas e o que passa a ser obrigatório.
```

ADRs não são editados depois de aceitos: uma nova decisão cria um novo ADR que substitui o anterior.

## Índice

| ADR | Título | Status |
|-----|--------|--------|
| [0001](./0001-monorepo.md) | Monorepo com pnpm workspaces + projeto Python | Aceito |
| [0002](./0002-imagem-unica-nginx-uvicorn.md) | Imagem Docker única com Nginx + Uvicorn via supervisord | Aceito |
| [0003](./0003-roteamento-por-prefixo-de-path.md) | Roteamento por prefixo de path | Aceito |
| [0004](./0004-ddd-no-backend.md) | DDD com bounded contexts e camadas no backend | Aceito |
| [0005](./0005-frontend-feature-based.md) | Frontends feature-based + pacotes compartilhados | Aceito |
| [0006](./0006-nextjs-static-export.md) | Next.js em modo static export (SPA) | Aceito |
| [0007](./0007-uv-e-pnpm.md) | uv e pnpm como gerenciadores | Aceito |
| [0008](./0008-convencao-de-nomes.md) | Convenção de nomes: camelCase no TS e na API, PEP 8 no Python | Proposto |
| [0009](./0009-contrato-openapi-gerado.md) | Contrato via OpenAPI gerado + cliente TS tipado | Aceito |
| [0010](./0010-protocolo-websocket.md) | Protocolo WebSocket com envelope `type/id/payload` | Aceito |
| [0011](./0011-padrao-branches-commits-mr.md) | GitLab, trunk-based, Conventional Commits e templates de MR | Aceito |
