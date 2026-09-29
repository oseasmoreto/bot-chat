# ADR-0004 — Configuração da API em runtime (não no build)

- **Status:** Aceito
- **Data:** 2026-09-29
- **Ticket:** CPBS-275

## Contexto
A URL da API muda por ambiente (`localhost:8000`, `api.<dominio>`…). Variáveis `NEXT_PUBLIC_*` são embutidas no JavaScript durante o build.

## Decisão
- `API_URL` e `WS_URL` lidas do ambiente do container pelo layout raiz (`getRuntimeConfig`, `server-only`), com `connection()` para renderizar por requisição.
- Entregues ao navegador por um `ConfigProvider` (contexto React); consumidas por `useApiClient()` e pelo cliente WS.
- `NEXT_PUBLIC_*` não são usadas.

## Alternativas consideradas
- **`NEXT_PUBLIC_*` no build:** uma imagem por ambiente — contraria "build once, deploy many".
- **Endpoint `/config.json` buscado no cliente:** requisição extra antes de qualquer chamada à API.

## Consequências
- Mesma imagem em todos os ambientes; erro explícito se a variável faltar.
- O layout raiz é dinâmico (renderizado a cada requisição) — custo baixo, pois a casca é pequena.
