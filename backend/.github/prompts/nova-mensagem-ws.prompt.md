---
description: "Cria um tipo de mensagem WebSocket (handler + registro no dispatcher), com análise, testes e protocolo documentado"
agent: backend-ddd
argument-hint: "type da mensagem, escopo e comportamento (ex.: partners.list no admin)"
---

Crie a mensagem WebSocket **${input:type:type no formato contexto.acao, ex.: partners.list}** no context **${input:context:ex.: partners}**.

Comportamento: ${input:comportamento:payload de entrada, resposta (type e payload), erros e escopos em que vale}

Siga o [agente backend-ddd](../agents/backend-ddd.agent.md) — fases **Análise → Plano → Construção → Validação** — e [presentation.instructions.md](../instructions/presentation.instructions.md#websocket).

## Fase 1 — Roteiro específico (além do roteiro comum do agente)

**Padrão da mensagem**
- [ ] É **requisição → resposta** (cliente envia, servidor responde com o mesmo `id`) ou **push** (servidor envia sem pedido)? Push exige saber para quem (conexão, usuário, todos do escopo) — hoje não há *pub/sub* entre réplicas; registrar se for necessário.
- [ ] `type` de entrada e de resposta (`<ctx>.<acao>` / `<ctx>.<resultado>`)?
- [ ] Vale em `public`, `admin` ou ambos? Comportamento muda por escopo?

**Payload**
- [ ] Campos de entrada (camelCase, tipo, obrigatório, limites) e exemplo.
- [ ] Campos da resposta (reaproveita um `…Response` do HTTP?) e exemplo.

**Erros e frequência**
- [ ] Falhas esperadas e `code` de cada uma (`invalid_payload`, `not_found`, regra de negócio).
- [ ] Frequência esperada (ex.: a cada digitação, a cada 15 s)? Precisa de limite?
- [ ] Já existe endpoint HTTP equivalente? (o handler reutiliza o mesmo caso de uso)

## Checklist de entrega

- [ ] Teste de integração antes (`tests/integration/websocket/test_<context>_ws.py`), com `headers={"origin": ALLOWED_ORIGIN}`: resposta com o mesmo `id`, payload inválido (`invalid_payload`) e regra por escopo, se houver.
- [ ] Handler em `presentation/ws_handlers.py` chamando um caso de uso (o mesmo do HTTP, se existir) — sem lógica duplicada.
- [ ] Payload validado com schema `BaseSchema`; resposta com `model_dump(mode="json", by_alias=True)`.
- [ ] `dispatcher.register("<type>", Handler(...))` em `api/container.py`.
- [ ] `docs/06-contratos-api.md`: tabela de mensagens e códigos de erro WS.
- [ ] Validação completa.
