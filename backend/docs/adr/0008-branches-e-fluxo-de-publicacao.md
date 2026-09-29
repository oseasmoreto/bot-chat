# ADR-0008 — Branches `developer`, `staging`, `master` e fluxo de publicação

- **Status:** Aceito
- **Data:** 2026-09-29

## Contexto
O time precisa de ambientes separados de desenvolvimento, homologação e produção, com controle explícito do que chega a cada um e rastreabilidade de cada mudança até o ticket.

## Decisão
- Três branches **permanentes e protegidas** (sem push direto, sem force push, não removíveis), cada uma ligada a um ambiente:
  - `developer` → **development** (branch padrão; recebe os MRs das branches de trabalho);
  - `staging` → **staging/homologação** (recebe só promoção da `developer`);
  - `master` → **production** (recebe só promoção da `staging` e `hotfix/*`).
- Publicação: `developer → staging → master` por **MRs de promoção** (template *Release*).
- **Todos os MRs** (trabalho, hotfix, promoção e back-merge) usam **merge commit**; squash fica **desabilitado** no projeto. Todo commit vai para o histórico, então todo commit segue o padrão (Conventional Commits + `Refs: CPBS-xxx`) e ajustes de revisão entram como novos commits.
- **Hotfix** sai da `master`, volta para a `master` e é obrigatoriamente levado de volta por **back-merge** `master → staging → developer`.
- Tags de versão `backend-vX.Y.Z` **somente na `master`**; o deploy em production é feito a partir da tag, com **aprovação manual**. `developer` e `staging` fazem deploy automático.
- A matriz origem → destino (e a ausência de squash) é validada no CI (`scripts/check-mr-flow.sh`).

Detalhes: [CONTRIBUTING §1](../../CONTRIBUTING.md#1-branches-e-fluxo-de-publicação) e [11 — CI](../11-ci.md).

## Alternativas consideradas
- **Git Flow completo** (`develop`, `release/*`, `hotfix/*`): branches de release por versão adicionam cerimônia desnecessária para deploy contínuo por ambiente.
- **Fast-forward / rebase nas integrações:** histórico linear, mas incompatível com promoções e back-merges entre branches permanentes.

## Consequências
- O que vai para produção é exatamente o que foi validado em staging, commit a commit.
- Correções achadas em homologação passam pela `developer` e por uma nova promoção — nunca direto na `staging`.
- Esquecer o back-merge de um hotfix faz a correção sumir na próxima promoção: por isso ele faz parte do checklist do template *Hotfix*.
- O autor é responsável pela qualidade de cada commit (mensagem, uma mudança lógica por commit).
- Mudanças que dependem do frontend: o backend chega a cada ambiente **antes ou junto** do frontend.
