# Backend — Erros e logging

## Tratamento de erros

- Exceções de domínio herdam de `DomainError` (`core/errors.py`), com `code: str` estável.
- `register_error_handlers(app)` converte para o formato padrão (ver [Contratos de API — formato de erro](./05-contratos-api.md#formato-padrão-de-erro)).
- `RequestValidationError` (422) também é convertido para o formato padrão.
- Nunca expor stack trace na resposta; ele vai para o log.

## Logging

- Log estruturado em **JSON** no stdout (coletado pelo supervisord → Docker).
- Campos mínimos: `timestamp`, `level`, `logger`, `message`, `scope` (quando aplicável), `requestId`.
- Middleware gera/propaga `X-Request-ID` (o Nginx também repassa o seu `$request_id`).
