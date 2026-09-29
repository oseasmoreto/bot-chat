# ADR-0007 — Protocolo WebSocket com envelope type/id/payload

- **Status:** Aceito
- **Data:** 2026-09-29
- **Ticket:** CPBS-275

## Decisão
- Um endpoint por escopo: `/api/v1/ws/public`, `/api/v1/ws/admin`.
- Envelope JSON `{ "type": "contexto.acao", "id": "...", "payload": {} }`; resposta repete o `id`.
- `MessageDispatcher` roteia por `type` para handlers registrados no container (Open/Closed).
- Erros como mensagem `type: "error"` com `code` estável. Handlers reutilizam os casos de uso do HTTP.

## Alternativas consideradas
- **Socket.IO:** protocolo proprietário e dependência extra nos dois lados.
- **Um endpoint WS por funcionalidade:** multiplica conexões no cliente.

## Consequências
- Nova mensagem = novo handler + teste + linha na tabela de [06](../06-contratos-api.md#mensagens-da-cpbs-275).
- Escala horizontal com estado exigirá pub/sub (futuro ADR).
