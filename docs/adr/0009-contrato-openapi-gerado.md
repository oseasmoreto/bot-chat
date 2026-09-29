# ADR-0009 — Contrato via OpenAPI gerado + cliente TS tipado

- **Status:** Aceito
- **Data:** 2026-09-29
- **Ticket:** CPBS-275

## Contexto
Precisamos de OpenAPI/Swagger e de código altamente tipado nas duas pontas, sem tipos duplicados à mão.

## Decisão
- FastAPI gera o OpenAPI a partir dos schemas Pydantic (`/api/openapi.json`, Swagger em `/api/docs`).
- `make openapi` exporta para `packages/api-client/openapi.json` (versionado) e gera `schema.d.ts` com `openapi-typescript`.
- Frontend chama a API com `openapi-fetch` tipado por `paths`.
- Teste de contrato no backend falha se o arquivo versionado divergir.

## Alternativas consideradas
- **Tipos TS escritos à mão:** divergem silenciosamente.
- **Geradores de SDK completos (orval, openapi-generator):** mais código gerado e mais configuração do que precisamos.

## Consequências
- Mudança de contrato quebra a compilação do front imediatamente.
- WebSocket não é coberto pelo OpenAPI → tipos em `@bot-varejo/ws-client` + [backend/05-contratos-api.md](../backend/05-contratos-api.md#protocolo-websocket).
