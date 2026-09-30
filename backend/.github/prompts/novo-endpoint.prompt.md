---
description: "Cria um endpoint REST em um context existente, com análise, schemas, testes, OpenAPI e contrato documentado"
agent: backend-ddd
argument-hint: "método, recurso, escopo e comportamento (ex.: GET /partners/{id} no admin)"
---

Crie o endpoint **${input:endpoint:método e path relativo ao escopo, ex.: GET /partners/{partner_id}}** no escopo **${input:escopo:public, admin ou ambos}**, no context **${input:context:ex.: partners}**.

Comportamento esperado: ${input:comportamento:entrada, saída, regras e erros esperados}

Siga o [agente backend-ddd](../agents/backend-ddd.agent.md) — fases **Análise → Plano → Construção → Validação** — e [presentation.instructions.md](../instructions/presentation.instructions.md).

## Fase 1 — Roteiro específico (além do roteiro comum do agente)

**Recurso e operação**
- [ ] Método e path corretos para a operação (GET lê, POST cria, PUT substitui, PATCH altera parte, DELETE remove)? Recurso no plural em kebab-case?
- [ ] `operationId` proposto (camelCase com escopo, ex.: `getAdminPartner`) — ele vira nome de função no frontend.
- [ ] Qual caso de uso atende? Existe ou precisa ser criado?

**Entrada**
- [ ] Parâmetros de path, query e corpo: nome (camelCase no JSON), tipo, obrigatório, formato, limites, valor padrão.
- [ ] Listagem: paginação (cursor opaco, tamanho padrão e máximo), filtros e ordenação?

**Saída**
- [ ] Status de sucesso (`200`, `201` com o recurso criado, `204` sem corpo)?
- [ ] Campos da resposta (reaproveita um `…Response` existente?) e exemplo de JSON.

**Erros**
- [ ] Cada falha com status e `code`: não encontrado (404), conflito/concorrência (409), regra de negócio (422 com `code` próprio), validação (422 `validation_error`).

**Comportamento**
- [ ] Idempotência: o que acontece se o mesmo POST chegar duas vezes?
- [ ] O frontend já consome algo parecido? Mudança compatível? Ticket do frontend?

## Checklist de entrega

- [ ] Teste de integração escrito antes (`tests/integration/api/test_<context>.py`): sucesso, cada erro esperado (formato `{"error": {"code", "message", "requestId"}}`) e os dois escopos se aplicável.
- [ ] Caso de uso existente reutilizado ou criado (com teste unitário).
- [ ] `schemas.py`: `…Request`/`…Response` com `BaseSchema` e `from_domain`.
- [ ] `http.py`: `async def`, `summary` pt-BR, `operation_id` camelCase com escopo, retorno anotado, `status_code` e `responses=` dos erros.
- [ ] Path plural em kebab-case; router incluído em `api/routes/public.py` e/ou `admin.py`.
- [ ] `openapi.json` regenerado (`python -m api.scripts.export_openapi openapi.json`).
- [ ] `docs/06-contratos-api.md`: tabela de endpoints, schema e códigos de erro.
- [ ] Validação completa (ruff, mypy, lint-imports, pytest ≥ 90%).
