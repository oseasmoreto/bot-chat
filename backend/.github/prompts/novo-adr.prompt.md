---
description: "Registra uma decisão de arquitetura: cria uma ADR nova ou reescreve a ADR existente com a decisão vigente, e atualiza os docs afetados"
agent: docs-backend
argument-hint: "a decisão (ex.: usar Redis para pub/sub do WebSocket entre réplicas)"
---

Registre a decisão: ${input:decisao:o que foi decidido e por quê}

Siga o [agente docs-backend](../agents/docs-backend.agent.md) — fases **Análise → Plano → Escrita → Validação** — e a seção *ADRs* de [docs.instructions.md](../instructions/docs.instructions.md#adrs).

## Fase 1 — Roteiro específico (além do roteiro comum do agente)

**Decisão**
- [ ] A decisão **já foi tomada** (por quem, quando)? Se ainda está em discussão, pare: ADR registra só decisão tomada.
- [ ] É nova ou **muda uma ADR existente**? (liste as ADRs em `docs/adr/README.md`; se muda, a ADR existente é reescrita — sem ADR nova de transição)
- [ ] Enunciado da decisão em uma frase, no presente ("usamos…", "cada context tem…").

**Contexto e alternativas**
- [ ] Qual problema ou necessidade levou à decisão? Quais restrições (custo, prazo, equipe, plataforma)?
- [ ] Quais alternativas foram avaliadas e **por que não** foram adotadas? (só opções não adotadas — nunca a solução usada antes)

**Consequências**
- [ ] O que fica mais fácil e o que fica mais difícil? Algum risco ou limite conhecido?
- [ ] Quais docs, README, CONTRIBUTING, código de referência e instruções do Copilot mudam por causa dela?
- [ ] Precisa de variável de ambiente, lib ou mudança de contrato? (se sim, entra no plano)

## Entregáveis

1. `docs/adr/NNNN-<nome>.md` (nova, próximo número) ou a ADR existente reescrita — formato: Status, Data, Contexto, Decisão, Alternativas consideradas, Consequências.
2. Linha em `docs/adr/README.md`.
3. Docs afetados atualizados para refletir a decisão (e o que ficou obsoleto removido).
4. `tests/contract/test_docs.py` verde e resumo final.
