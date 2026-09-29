# 08 — Docker e deploy (backend)

Imagem própria do backend, baseada em **`python:3.13-slim`**, rodando **Uvicorn diretamente** — um processo por container ([ADR-0001](./adr/0001-imagem-python-uvicorn.md)). TLS e domínio (`api.<dominio>`) ficam na plataforma de deploy (load balancer/ingress).

## 1. Dockerfile multi-stage

```mermaid
flowchart LR
    base["base<br/>python:3.13-slim + uv"] --> dev["dev<br/>deps com grupo dev<br/>uvicorn --reload"]
    base --> builder["builder<br/>uv sync --no-dev<br/>→ .venv com o pacote"]
    builder -->|".venv"| runtime["runtime<br/>python:3.13-slim limpo<br/>usuário não-root · :8000"]
```

### `Dockerfile`

```dockerfile
# syntax=docker/dockerfile:1
ARG PYTHON_VERSION=3.13

# ---------- base ---------------------------------------------------------------
FROM python:${PYTHON_VERSION}-slim AS base
# Fixar a tag exata do uv na implementação (nunca usar :latest em produção)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=never
WORKDIR /app

# ---------- dev (docker-compose.dev.yml) ---------------------------------------
FROM base AS dev
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-install-project
ENV PATH=/app/.venv/bin:$PATH PYTHONPATH=/app/src
EXPOSE 8000
CMD ["uvicorn", "bot_varejo.main:create_app", "--factory", "--reload", "--reload-dir", "/app/src", "--host", "0.0.0.0", "--port", "8000"]

# ---------- builder ------------------------------------------------------------
FROM base AS builder
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-dev --no-install-project
COPY src ./src
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-dev --no-editable

# ---------- runtime (imagem final) ---------------------------------------------
FROM python:${PYTHON_VERSION}-slim AS runtime
ARG APP_VERSION=0.1.0
ENV APP_VERSION=${APP_VERSION} \
    PATH=/app/.venv/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    FORWARDED_ALLOW_IPS=127.0.0.1

RUN useradd --system --uid 10001 --no-create-home app
WORKDIR /app
COPY --from=builder --chown=app:app /app/.venv /app/.venv

USER app
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/v1/public/health', timeout=2)"]
CMD ["uvicorn", "bot_varejo.main:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
```

Pontos importantes:

- **Sem `curl`** na imagem: o HEALTHCHECK usa o próprio Python. `urlopen` falha em 503, então health `down` marca o container como *unhealthy*.
- **Não-root** (`app`, uid 10001).
- `--proxy-headers` + `FORWARDED_ALLOW_IPS`: o Uvicorn só confia em `X-Forwarded-*` vindos desses IPs. Em produção, configure com o IP/rede do load balancer (ou `*` se o container só for acessível pela rede privada).
- **1 processo Uvicorn** por container; escalar = mais réplicas. WebSocket com estado entre réplicas exigirá *pub/sub* (futuro).
- `.dockerignore`: `.venv`, `__pycache__`, `.pytest_cache`, `.mypy_cache`, `htmlcov`, `.coverage`, `docs/`, `tests/`.

## 2. Docker Compose

| Arquivo | Propósito | Comando |
|---------|-----------|---------|
| `docker-compose.yml` | Sobe a **imagem de runtime** (igual à produção) | `docker compose up --build` |
| `docker-compose.dev.yml` | Desenvolvimento com `--reload` e código montado | `docker compose -f docker-compose.dev.yml up --build` |

### `docker-compose.yml`

```yaml
name: bot-varejo-backend

services:
  api:
    build:
      context: .
      target: runtime
      args:
        APP_VERSION: ${APP_VERSION:-0.1.0}
    image: bot-varejo-backend:local
    ports:
      - "${API_PORT:-8000}:8000"
    env_file:
      - path: .env
        required: false
    restart: unless-stopped
```

### `docker-compose.dev.yml`

```yaml
name: bot-varejo-backend-dev

services:
  api:
    build:
      context: .
      target: dev
    ports:
      - "${API_PORT:-8000}:8000"
    volumes:
      - ./src:/app/src
    env_file:
      - path: .env
        required: false
```

> Mudou `pyproject.toml`/`uv.lock`? Suba de novo com `--build`.
>
> Os dois arquivos de compose incluem o serviço `dynamodb` (DynamoDB Local) quando houver persistência — definição e variáveis em [12 — Persistência](./12-persistencia-dynamodb.md#7-ambiente-local).

### Rodando junto com o frontend

Os dois projetos sobem de forma independente e conversam por `localhost`:

```mermaid
flowchart LR
    b["Navegador"] -->|"http://localhost:3000"| f["frontend<br/>(compose do frontend)"]
    b -->|"http://localhost:8000<br/>ws://localhost:8000"| a["api<br/>(compose do backend)"]
```

1. Aqui: `docker compose up --build` → API em `:8000` (CORS já libera `http://localhost:3000` por padrão).
2. No repositório do frontend: `docker compose up --build` → front em `:3000`.

O frontend também pode subir a API a partir da imagem publicada no registry (profile `api` do compose do frontend) — ver `docs/10-docker-deploy.md` no repositório do **frontend**.

## 3. Portas

| Porta | Onde | Exposta no host? |
|-------|------|------------------|
| 8000 | Uvicorn (runtime e dev) | ✅ (`API_PORT`) |
| 8001 | DynamoDB Local (compose; porta 8000 dentro da rede do compose) | ✅ (`DYNAMODB_PORT`) |

## 4. Variáveis de ambiente

Documentadas também em `.env.example`.

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `APP_ENV` | `local` | `local` · `dev` · `staging` · `production` |
| `APP_VERSION` | `0.1.0` | Versão exibida no health e no OpenAPI (injetada no build pela tag) |
| `APP_LOG_LEVEL` | `INFO` | `DEBUG` · `INFO` · `WARNING` · `ERROR` |
| `APP_DOCS_ENABLED` | `true` | Liga `/api/docs`, `/api/redoc`, `/api/openapi.json` |
| `APP_CORS_ORIGINS` | `["http://localhost:3000"]` | Origens do frontend (JSON). Vale para CORS e para o `Origin` do WebSocket |
| `FORWARDED_ALLOW_IPS` | `127.0.0.1` | IPs de proxy confiáveis para `X-Forwarded-*` (lido pelo Uvicorn) |
| `API_PORT` | `8000` | Porta publicada no host (compose) |
| `APP_AWS_REGION` | `sa-east-1` | Região do DynamoDB ([12](./12-persistencia-dynamodb.md#6-configuração)) |
| `APP_DYNAMODB_ENDPOINT_URL` | `http://dynamodb:8000` (local) | Endpoint do DynamoDB Local; vazio na AWS |
| `APP_DYNAMODB_TABLE_PREFIX` | `bot-varejo-local` | Prefixo das tabelas (`<prefixo>-<context>`) |
| `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` | `local` (só local) | Na AWS, credenciais vêm da role IAM |
| `DYNAMODB_PORT` | `8001` | Porta do DynamoDB Local no host (compose) |

## 5. Entrega por ambiente

Cada branch permanente publica no seu ambiente ([CONTRIBUTING §1](../CONTRIBUTING.md#1-branches-e-fluxo-de-publicação)):

```mermaid
flowchart LR
    mr["MR de trabalho<br/>merge na developer"] --> dev["developer<br/>imagem :developer<br/>deploy development"]
    dev -->|"MR de promoção"| stg["staging<br/>imagem :staging<br/>deploy staging"]
    stg -->|"MR de promoção"| mst["master<br/>imagem :master"]
    mst -->|"tag backend-vX.Y.Z"| prod["imagem :X.Y.Z<br/>deploy production<br/>(aprovação manual)"]
```

| Ambiente | Branch | Imagem | URL (convenção) | Deploy |
|----------|--------|--------|-----------------|--------|
| development | `developer` | `backend:developer` | `https://api-dev.<dominio>` | automático |
| staging | `staging` | `backend:staging` | `https://api-staging.<dominio>` | automático |
| production | `master` (tag) | `backend:X.Y.Z` | `https://api.<dominio>` | manual (aprovação) |

A mesma imagem roda em qualquer ambiente: o que muda são as **variáveis de ambiente** configuradas em cada um (§4). Detalhes do pipeline em [11 — CI](./11-ci.md).
