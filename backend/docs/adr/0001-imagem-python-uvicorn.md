# ADR-0001 — Imagem python:3.13-slim com Uvicorn

- **Status:** Aceito
- **Data:** 2026-09-29

## Contexto
A API tem domínio próprio (`api.<dominio>`) e só expõe REST e WebSocket: não há arquivos estáticos para servir. TLS e domínio são tratados pela plataforma de deploy (load balancer/ingress).

## Decisão
- Imagem multi-stage baseada em `python:3.13-slim`, com as dependências instaladas por pip num venv do estágio de build.
- Um processo por container: **Uvicorn** servindo o FastAPI na porta 8000.
- Usuário não-root; HEALTHCHECK em Python puro; `--proxy-headers` + `FORWARDED_ALLOW_IPS`.

## Alternativas consideradas
- **Gunicorn + workers Uvicorn:** útil para vários workers por container; preferimos escalar por réplicas (KISS), revisitável.

## Consequências
- Imagem pequena e simples de operar.
- Escala horizontal por réplicas; WebSocket com estado exigirá pub/sub no futuro.
