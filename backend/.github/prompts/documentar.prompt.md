---
description: "Cria ou atualiza a documentação do backend (docs, README, CONTRIBUTING, glossário, tarefas) a partir de uma mudança ou assunto, com análise e validação"
agent: docs-backend
argument-hint: "o que documentar (ex.: as mudanças da branch atual, o novo context partners, como rodar sem Docker)"
---

Documente: ${input:assunto:o que documentar — ex.: as mudanças pendentes da branch, um context novo, um guia}

Siga o [agente docs-backend](../agents/docs-backend.agent.md) — fases **Análise → Plano → Escrita → Validação** — e [docs.instructions.md](../instructions/docs.instructions.md).

## Fase 1 — Roteiro específico (além do roteiro comum do agente)

**Mudança de código** (quando o assunto vem de um diff/branch)
- [ ] Leia `git diff` e `git status`: quais arquivos de código, contrato e configuração mudaram?
- [ ] Cada mudança está refletida no doc certo? (endpoint/mensagem → `06`; estrutura → `02`; erro → `07`; variável → `08` + `.env.example` + README; lib → `13`; context → `01`/`02`/`03`)
- [ ] Algum trecho de código embutido nos docs ficou diferente do arquivo real?

**Guia ou explicação** (quando o assunto é um tema)
- [ ] Qual pergunta o leitor quer responder ao abrir o doc? (vira o título e a primeira frase)
- [ ] Qual o passo a passo mínimo, com comandos para cada sistema, e como conferir que deu certo?
- [ ] Quais problemas comuns entram na seção de solução de problemas (sintoma → causa → solução)?

**Tarefa** (quando há ticket)
- [ ] Enunciado, objetivo, análise, critérios de aceitação, definição de pronto, fora de escopo e entregáveis para `docs/tasks/CPBS-<n>-<slug>.md`?

## Entregáveis

1. Docs criados/atualizados e o que ficou obsoleto removido.
2. Índices (`docs/README.md`, `docs/adr/README.md`, `docs/tasks/README.md`), glossário e `docs/02-estrutura.md` atualizados quando aplicável.
3. Instruções do Copilot em `.github/` ajustadas se a regra documentada mudou.
4. `tests/contract/test_docs.py` verde e resumo final.
