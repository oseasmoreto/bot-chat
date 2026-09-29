# ADR-0010 — Protocolo WebSocket com envelope type/id/payload

- **Status:** Aceito
- **Data:** 2026-09-29
- **Ticket:** CPBS-275

## Contexto
O chat será tempo real. Precisamos de um formato de mensagem extensível desde o primeiro endpoint (health).

## Decisão
- Um endpoint por escopo: `/ws/public`, `/ws/admin`.
- Envelope JSON `{ "type": "contexto.acao", "id": "...", "payload": {} }`; resposta repete o `id`.
- `MessageDispatcher` roteia por `type` para handlers registrados no container (Open/Closed).
- Erros como mensagem `type: "error"` com `code` estável.
- Handlers reutilizam os casos de uso do HTTP.

## Alternativas consideradas
- **Socket.IO:** adiciona protocolo proprietário e dependência no cliente e servidor.
- **Um endpoint WS por funcionalidade:** multiplica conexões no cliente.

## Consequências
- Nova mensagem = novo handler + teste + linha na tabela de [backend/05-contratos-api.md](../backend/05-contratos-api.md#protocolo-websocket).
- Escala horizontal com estado de conexão exigirá pub/sub (futuro ADR).
