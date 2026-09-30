# syntax=docker/dockerfile:1
ARG PYTHON_VERSION=3.13

# ---------- base ---------------------------------------------------------------
FROM python:${PYTHON_VERSION}-slim AS base
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app

# ---------- dev (docker-compose.dev.yml) ---------------------------------------
FROM base AS dev
COPY requirements.txt requirements-test.txt ./
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements-test.txt
ENV PYTHONPATH=/app \
    PYTHONDONTWRITEBYTECODE=1
EXPOSE 8000
CMD ["uvicorn", "api.app_run:create_app", "--factory", "--reload", "--reload-dir", "/app/api", "--host", "0.0.0.0", "--port", "8000"]

# ---------- builder ------------------------------------------------------------
FROM base AS builder
RUN python -m venv /app/.venv
ENV PATH=/app/.venv/bin:$PATH
COPY requirements.txt ./
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

# ---------- runtime (imagem final) ---------------------------------------------
FROM python:${PYTHON_VERSION}-slim AS runtime
ARG APP_VERSION=0.0.0-local
ENV APP_VERSION=${APP_VERSION} \
    PATH=/app/.venv/bin:$PATH \
    PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    FORWARDED_ALLOW_IPS=127.0.0.1

RUN useradd --system --uid 10001 --no-create-home app
WORKDIR /app
# Código e dependências ficam com dono root: o usuário da aplicação só lê.
COPY --from=builder /app/.venv /app/.venv
COPY api ./api
RUN python -m compileall -q api

USER app
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/v1/public/health', timeout=2)"]
CMD ["uvicorn", "api.app_run:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
