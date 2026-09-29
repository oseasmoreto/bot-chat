# ADR-0007 — Cliente HTTP tipado gerado do OpenAPI do backend

- **Status:** Aceito
- **Data:** 2026-09-29
- **Ticket:** CPBS-275

## Contexto
Front e back são projetos separados; tipos escritos à mão divergem silenciosamente do contrato.

## Decisão
- `pnpm openapi` baixa o `/api/openapi.json` da API (local ou dev), salva em `src/shared/api/openapi.json` (versionado) e gera `schema.d.ts` com `openapi-typescript`.
- Chamadas via `openapi-fetch` tipado por `paths`; tipos de domínio derivados de `components['schemas']`.
- WebSocket: tipos próprios em `src/shared/ws` seguindo o protocolo documentado no backend.

## Alternativas consideradas
- **Geradores de SDK completos (orval, openapi-generator):** mais código gerado e configuração.
- **Copiar o `openapi.json` à mão do repositório do backend:** sujeito a esquecimento e sem garantir que corresponde à API rodando.

## Consequências
- Mudança de contrato quebra a compilação do front no próximo `pnpm openapi`.
- O diff de `openapi.json` no MR do front mostra exatamente o que mudou na API.
