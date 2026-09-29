# ADR-0002 — Domínio próprio da API, CORS e validação de Origin

- **Status:** Aceito
- **Data:** 2026-09-29
- **Ticket:** CPBS-275

## Contexto
O frontend (`app.<dominio>`) chama a API (`api.<dominio>`) diretamente do navegador: são origens diferentes.

## Decisão
- Todas as rotas da aplicação sob o prefixo **`/api`**, seguido da **versão**: REST `/api/v1/{public|admin}/...`, WebSocket `/api/v1/ws/{public|admin}` e documentação `/api/docs`, `/api/redoc`, `/api/openapi.json`. REST e WebSocket evoluem juntos na mesma versão.
- `CORSMiddleware` com lista explícita de origens em `APP_CORS_ORIGINS` (nunca `*`), `allow_credentials=True`.
- WebSocket: handshake recusado (código `1008`) se o header `Origin` não estiver na mesma lista — proteção contra *Cross-Site WebSocket Hijacking*, já que CORS não se aplica a WS.

## Alternativas consideradas
- **Proxy no frontend (rewrites do Next para a API):** evitaria CORS, mas faria todo tráfego (inclusive WS) passar pelo servidor Node do front e acoplaria os deploys.

## Consequências
- Cada ambiente precisa configurar `APP_CORS_ORIGINS` com o domínio do frontend.
- Clientes WS sem `Origin` (ex.: scripts) precisam enviar o header — documentado no README.
- Cookies de sessão futuros: `SameSite=Lax; Secure; Domain=.<dominio>` (mesmo site) — decisão no ADR de autenticação.
