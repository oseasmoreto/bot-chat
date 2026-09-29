# ADR-0006 — Contrato via OpenAPI gerado, versionado e publicado

- **Status:** Aceito
- **Data:** 2026-09-29

## Contexto
Front e back são projetos separados; o front precisa de tipos confiáveis sem escrevê-los à mão.

## Decisão
- FastAPI gera o OpenAPI a partir dos schemas Pydantic (`/api/openapi.json`, Swagger em `/api/docs`).
- `make openapi` exporta para `openapi.json` na raiz do repositório (versionado); teste de contrato falha se divergir do código.
- O frontend gera seus tipos a partir do `/api/openapi.json` da API rodando (local ou dev).
- Mudança incompatível = nova versão de rota (`/api/v2`) convivendo com a anterior.

## Consequências
- Toda mudança de contrato aparece no diff do MR do backend.
- WebSocket não é coberto pelo OpenAPI → protocolo documentado em [06](../06-contratos-api.md#protocolo-websocket).
