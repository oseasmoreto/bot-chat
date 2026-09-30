<!--
  BACKEND — RELEASE: promoção (developer → staging, staging → master) ou back-merge (master → staging, staging → developer).
  Título:
    chore: promove developer para staging
    chore: promove staging para master (backend-vX.Y.Z)
    chore: back-merge master para staging
    chore: back-merge staging para developer
  ⚠️ NÃO apagar a branch de origem. Merge feito por Maintainer.
  Guia: CONTRIBUTING.md §1.6 e §1.7
-->

## 🚀 Tipo

- [ ] Promoção `developer → staging` (homologação)
- [ ] Promoção `staging → master` (produção após a tag)
- [ ] Back-merge `master → staging` (pós-hotfix)
- [ ] Back-merge `staging → developer` (pós-hotfix)

**Versão (se → master):** `backend-v` <!-- X.Y.Z — feat → minor · fix/perf → patch · breaking → major -->

## 📦 Conteúdo

<!-- Saída de: git log --oneline --no-merges origin/<destino>..origin/<origem> -->

| MR | Ticket | Tipo | Descrição |
|----|--------|------|-----------|
| !  | CPBS-  |      |           |

## 🔌 Contrato com o frontend

- [ ] Nenhuma mudança de contrato neste release
- [ ] Mudanças de contrato **retrocompatíveis** com o frontend que já está no ambiente de destino: <!-- endpoints / mensagens WS -->
- [ ] Frontend dependente será promovido **depois** deste release: <!-- MR/ticket do frontend -->

## ⚙️ Configuração do ambiente de destino

- [ ] Sem variáveis novas
- [ ] Variáveis novas/alteradas já configuradas no ambiente: <!-- APP_*, APP_CORS_ORIGINS… -->
- [ ] Tabelas/índices novos do DynamoDB já criados no ambiente (IaC aplicada): <!-- quais -->

## ✅ Validação

**Antes do merge**

- [ ] Validação completa da branch de origem verde (lint, tipos, testes)
- [ ] Ambiente de origem saudável (`/api/v1/public/health`, `/api/v1/admin/health`, WebSocket)
- [ ] (→ master) Homologação em **staging** concluída — responsável / evidência: <!-- link -->

**Depois do merge**

- [ ] Nova versão rodando no ambiente de destino
- [ ] Health dos escopos `public` e `admin` = `ok`; WebSocket respondendo `health.pong`
- [ ] (→ master) Tag `backend-vX.Y.Z` criada no commit de merge
- [ ] (back-merge) Correção do hotfix presente na branch de destino

## ↩️ Rollback

- Versão atual no ambiente de destino: `backend-v`
- Rollback para: `backend-v`

## 🔗 MRs relacionados

<!-- Release do frontend no mesmo ambiente, hotfix que originou o back-merge… -->

## ✅ Checklist do release

- [ ] Título no formato `chore: promove …` / `chore: back-merge …`
- [ ] **"Delete source branch" desmarcado**
- [ ] Origem → destino permitidos pela matriz (CONTRIBUTING §1.3)
- [ ] Aprovações: ≥ 1 Maintainer (→ master: 2)

/assign me
