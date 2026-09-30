# 07 — Erros e logging

## Tratamento de erros

As exceções de negócio ficam em `api/core/exceptions.py` (Python puro, importável pelo domínio). Os handlers ficam em `api/core/errors.py`: `register_error_handlers(app)` converte toda exceção para o [formato padrão de erro](./06-contratos-api.md#formato-padrão-de-erro); nunca expõe stack trace na resposta (ele vai para o log).

### Exceções de negócio

Domínio e casos de uso levantam exceções que herdam de `DomainError` (`api.core.exceptions`), com `code` estável (snake_case, faz parte do contrato):

| Exceção | `code` | HTTP |
|---------|--------|------|
| `DomainError` (base) | `domain_error` | 422 |
| `NotFoundError` | `not_found` | 404 |
| `ConflictError` | `conflict` | 409 |

Um erro novo = subclasse com `code` e `status_code` próprios, no `domain/errors.py` do context:

```python
from http import HTTPStatus

from api.core.exceptions import DomainError


class PartnerInactiveError(DomainError):
    code = "partner_inactive"
    status_code = HTTPStatus.UNPROCESSABLE_ENTITY


raise PartnerInactiveError("Parceiro inativo")
```

### Erros do framework

| Situação | HTTP | `code` |
|----------|------|--------|
| Dados de entrada inválidos (`RequestValidationError`) | 422 | `validation_error` — `details` com `field` (ex.: `query.limit`) e `message` |
| Rota inexistente | 404 | `not_found` |
| Método não suportado | 405 | `method_not_allowed` (mantém o header `Allow`) |
| Outros `HTTPException` | status original | `bad_request`, `unauthorized`, `forbidden`, `conflict`, `payload_too_large`, `unsupported_media_type`, `too_many_requests` ou `http_error` |
| Exceção inesperada | 500 | `internal_error` — mensagem genérica; stack trace no log (`http.unhandled_error`) |

## Logging

- Log estruturado em **JSON**, uma linha por evento, no stdout (`api/core/logs.py`) — coletado pelo Docker/plataforma de deploy. Os logs do Uvicorn (acesso e erros) saem no mesmo formato.
- Campos: `timestamp` (UTC, ISO 8601), `level`, `logger`, `message`, `requestId` (quando há requisição) e os campos passados em `extra=` (ex.: `scope`); `exception` quando há stack trace.
- Nível por `APP_LOG_LEVEL`.
- Mensagens como eventos curtos em `contexto.acao` (`ws.rejected_origin`, `http.unhandled_error`), com dados em `extra=`, nunca concatenados no texto.

```json
{"timestamp": "2026-09-30T12:45:22.397645+00:00", "level": "WARNING", "logger": "api.routes.websocket", "message": "ws.rejected_origin", "requestId": "0daf86cb9a48473da93231ccfe209a02", "scope": "public"}
```

## `X-Request-ID`

`RequestIdMiddleware` (`api/core/request_id.py`, ASGI puro — vale para HTTP e para o handshake do WebSocket):

- Reaproveita o `X-Request-ID` recebido (load balancer ou frontend) se tiver até 128 caracteres entre `A-Z a-z 0-9 . _ -`; senão gera um novo (UUID4 em hex, 32 caracteres). Isso impede injeção de texto no log e em headers.
- Devolve o valor no header `X-Request-ID` da resposta — exposto via CORS para o front poder logar.
- Disponível no log (`requestId`) e no corpo de erro (`error.requestId`).
