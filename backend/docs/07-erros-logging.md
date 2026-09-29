# 07 — Erros e logging

## Tratamento de erros

- Exceções de domínio herdam de `DomainError` (`core/errors.py`), com `code: str` estável.
- `register_error_handlers(app)` converte para o formato padrão (ver [Contratos de API — formato de erro](./06-contratos-api.md#formato-padrão-de-erro)).
- `RequestValidationError` (422) também é convertido para o formato padrão.
- Nunca expor stack trace na resposta; ele vai para o log.

## Logging

- Log estruturado em **JSON** no stdout (coletado pelo Docker/plataforma de deploy).
- Campos mínimos: `timestamp`, `level`, `logger`, `message`, `scope` (quando aplicável), `requestId`.
- Middleware gera ou propaga `X-Request-ID` (se o load balancer ou o frontend enviarem, o valor é reaproveitado) e o devolve na resposta — exposto via CORS para o front poder logar.
