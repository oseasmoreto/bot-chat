# ADR-0002 — Imagem Docker única com Nginx + Uvicorn via supervisord

- **Status:** Aceito
- **Data:** 2026-09-29
- **Ticket:** CPBS-275

## Contexto
A task exige uma única imagem e um único deploy, e também exige Nginx para roteamento. Foi definido que o **FastAPI cuida apenas de APIs e WebSocket**; roteamento e arquivos estáticos são responsabilidade do Nginx.

## Decisão
Dockerfile multi-stage gera uma imagem final com:
- Nginx (porta 8080) servindo os builds estáticos de `web` e `admin` e fazendo proxy de `/api` e `/ws`;
- Uvicorn/FastAPI em `127.0.0.1:8000` (não exposto);
- supervisord como PID 1, com *eventlistener* que derruba o container se um processo entrar em FATAL.

## Alternativas consideradas
- **FastAPI servindo o build estático (StaticFiles):** descartado pelo time — mistura responsabilidades.
- **Duas imagens (nginx + api):** mais "um processo por container", mas foge do requisito de imagem única.
- **s6-overlay / tini + script:** alternativas ao supervisord; supervisord é mais conhecido e suficiente.

## Consequências
- Um artefato, um deploy, um healthcheck (que passa pelo Nginx e valida os dois processos).
- Escalar API e estáticos separadamente não é possível nesta arquitetura (aceitável agora).
- Container roda como não-root; Nginx configurado para `/tmp` (pid, temporários).
