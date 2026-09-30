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
- Tags de versão `frontend-vX.Y.Z` **somente na `master`**: a tag identifica a versão que vai para production.
- A matriz origem → destino é garantida pelas permissões das branches protegidas e pela revisão; o squash fica desabilitado nas configurações do GitLab.

Detalhes: [CONTRIBUTING §1](../../CONTRIBUTING.md#1-branches-e-fluxo-de-publicação).

## Alternativas consideradas
- **Git Flow completo** (`develop`, `release/*`, `hotfix/*`): branches de release por versão adicionam cerimônia desnecessária para entregas contínuas por ambiente.
- **Fast-forward / rebase nas integrações:** histórico linear, mas incompatível com promoções e back-merges entre branches permanentes.

## Consequências
- O que vai para produção é exatamente o que foi validado em staging, commit a commit.
- Correções achadas em homologação passam pela `developer` e por uma nova promoção — nunca direto na `staging`.
- Esquecer o back-merge de um hotfix faz a correção sumir na próxima promoção: por isso ele faz parte do checklist do template *Hotfix*.
- O autor é responsável pela qualidade de cada commit (mensagem, uma mudança lógica por commit).
- O frontend só chega a um ambiente depois do backend de que depende — o E2E contra o ambiente implantado confirma isso.
