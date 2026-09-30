---
applyTo: "api/contexts/**/presentation/**,api/routes/**"
description: "Camada presentation e api/routes: routers FastAPI, schemas Pydantic, handlers WebSocket, composição por escopo"
---

# Camada `presentation` e `api/routes/`

Referência: `api/contexts/health/presentation/` e `api/routes/`.

## Arquivos do context

| Arquivo | Conteúdo |
|---------|----------|
| `schemas.py` | `<Nome>Request` / `<Nome>Response` herdando de `BaseSchema` (`api.core.schemas`) — camelCase automático; `Response.from_domain(entidade)` como `@classmethod` |
| `dependencies.py` | Funções `get_<caso_de_uso>(container = Depends(get_container))` que devolvem o caso de uso do `Container` |
| `http.py` | `build_<ctx>_router(scope: Scope) -> APIRouter` quando o recurso existe nos dois escopos; senão `build_<ctx>_admin_router()` / `build_<ctx>_public_router()` |
| `ws_handlers.py` | Classes `<Acao>Handler` com `async def __call__(self, message: WsMessage, scope: Scope) -> WsMessage` |

## Rotas HTTP

- O router do context define o recurso (`APIRouter(prefix="/partners", tags=["partners"])`); os prefixos `/api/v1/public` e `/api/v1/admin` ficam **só** em `api/routes/public.py` e `api/routes/admin.py`, que fazem `include_router(...)`.
- Todo endpoint: `async def`, `summary` em pt-BR, `operation_id` camelCase único com o escopo (`listAdminPartners`), tipo de retorno anotado (`-> PartnerResponse`), `status_code` explícito em criação (`201`) e `responses={...}` para erros esperados (404, 409, 422 de negócio).
- Path em kebab-case e plural; parâmetros de query com `Annotated[int, Query(ge=1, le=100)]`.
- O handler só traduz: schema de entrada → comando/caso de uso → entidade → `Response.from_domain(...)`. Sem regra de negócio, sem acesso a adapter.
- Erros: deixe as exceções de `DomainError` subirem — `register_error_handlers` monta a resposta padrão. Nunca `raise HTTPException(...)` para erro de negócio.
- **Nunca** importe `infrastructure`: tudo chega via `Depends` do `dependencies.py`.

## WebSocket

- Handler novo = classe em `ws_handlers.py` + registro em `api/container.py`: `dispatcher.register("<ctx>.<acao>", Handler(caso_de_uso))`.
- Valide o `payload` com um schema `BaseSchema` (`Request.model_validate(message.payload)`); payload inválido responde `ws_error("invalid_payload", ...)` com o mesmo `id`.
- Resposta: `WsMessage(type="<ctx>.<acao_resultado>", id=message.id, payload=Response.from_domain(...).model_dump(mode="json", by_alias=True))`.
- Os endpoints `/api/v1/ws/{public,admin}` (em `api/routes/websocket.py`) não mudam: o roteamento é pelo `type`.

## Depois de mudar o contrato

1. Testes de integração: `tests/integration/api/test_<ctx>.py` (HTTP, os dois escopos quando aplicável) e `tests/integration/websocket/test_<ctx>_ws.py`.
2. `python -m api.scripts.export_openapi openapi.json` e commitar o `openapi.json`.
3. Atualizar `docs/06-contratos-api.md` (endpoints, schemas, mensagens WS, códigos de erro).
