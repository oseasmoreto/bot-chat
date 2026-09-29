# ADR-0011 — GitLab, trunk-based, Conventional Commits e templates de MR

- **Status:** Aceito
- **Data:** 2026-09-29
- **Ticket:** CPBS-275

## Contexto
O time trabalha com merge requests no **GitLab** e tickets no Jira (`CPBS-xxx`). Precisamos de um histórico legível, rastreável até o ticket, e de um processo de revisão consistente entre backend, web, admin e infra.

## Decisão
- **Plataforma:** GitLab (repositório, MR, GitLab CI, Container Registry).
- **Branches:** trunk-based; `main` protegida; branches curtas `<tipo>/CPBS-<n>-<descricao>`; `hotfix/` para urgências em produção.
- **Commits:** Conventional Commits em pt-BR, escopos por parte do monorepo, rodapé `Refs: CPBS-<n>` obrigatório.
- **MR:** título no formato de commit; templates `Default`, `Bugfix`, `Hotfix`, `Docs` em `.gitlab/merge_request_templates/`; squash + fast-forward.
- **Versões:** tags SemVer na `main`, derivadas dos tipos de commit.
- **Garantia:** commitlint e validação de branch em hooks locais (pre-commit) **e** no job `validate:mr` do CI.

Detalhes em [08 — Branches, commits e merge requests](../08-branches-commits-mr.md).

## Alternativas consideradas
- **Git Flow (`develop`, `release/*`):** mais cerimônia e merges longos; desnecessário com deploy único e contínuo a partir da `main`.
- **Merge commit sem squash:** histórico poluído por commits intermediários ("wip", "ajuste").
- **Sem padrão de commit:** impede versionamento/changelog automáticos e rastreabilidade.
- **Husky para hooks:** o projeto já usa `pre-commit` (backend Python); um único gerenciador de hooks para o monorepo inteiro.

## Consequências
- Todo trabalho exige um ticket.
- O título do MR precisa estar correto, pois vira o commit na `main`.
- Aprovações obrigatórias por caminho e *push rules* dependem do plano do GitLab; no Free valem por convenção + CI.
- Changelog automático passa a ser possível no futuro.
