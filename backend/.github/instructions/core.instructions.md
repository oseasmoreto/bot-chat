---
applyTo: "main.py,api/core/**,api/app_run.py,api/config.py,api/container.py"
description: "Shared kernel (api/core), composição da aplicação, configuração e container"
---

# `api/core/`, `app_run.py`, `config.py`, `container.py`

- `core/` é o *shared kernel*: só o que é transversal a **todos** os contexts (CORS, Swagger, logs, erros, `X-Request-ID`, `Scope`, `BaseSchema`, WebSocket, acesso ao DynamoDB). Algo usado por um context só fica no context.
- `core/scope.py` e `core/exceptions.py` são importados pelo domínio: mantenha-os **Python puro** (sem FastAPI, Pydantic, boto, httpx).
- `core/errors.py` converte exceções em respostas; código de erro novo do framework entra em `_HTTP_ERROR_CODES`.
- Middleware novo: ASGI puro (não `BaseHTTPMiddleware`) para valer também no WebSocket; registrado em `app_run.py` respeitando a ordem (o último `add_middleware` é o mais externo).
- `config.py`: variável nova = campo tipado no `Settings` com padrão seguro para local (`APP_<NOME>`), documentada em `.env.example` e em `docs/08-docker.md` (§4). Segredo sem valor padrão.
- `container.py` é o **único** lugar que instancia adapters e casos de uso: adicione o campo ao `Container` e monte em `build_container(settings)`. Recursos com ciclo de vida (clientes HTTP, DynamoDB) abrem/fecham no `lifespan` de `app_run.py`.
- `main.py` (raiz) só sobe a aplicação: expõe `app` e `run()` (`python main.py`). Nada de rota, middleware ou regra ali.
- `app_run.py` só compõe: middlewares, `include_router`, handlers de erro. Nada de rota ou regra aqui.
- Mudou algo aqui? Teste em `tests/unit/core/` ou `tests/integration/api/`.
