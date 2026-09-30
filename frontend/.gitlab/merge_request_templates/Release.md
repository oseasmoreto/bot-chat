<!--
  FRONTEND — RELEASE: promoção (developer → staging, staging → master) ou back-merge (master → staging, staging → developer).
  Título:
    chore: promove developer para staging
    chore: promove staging para master (frontend-vX.Y.Z)
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

**Versão (se → master):** `frontend-v` <!-- X.Y.Z — feat → minor · fix/perf → patch · breaking → major -->

## 📦 Conteúdo

<!-- Saída de: git log --oneline --no-merges origin/<destino>..origin/<origem> -->

| MR | Ticket | Área | Descrição |
|----|--------|------|-----------|
| !  | CPBS-  | web / admin / frontend | |

**Telas novas/alteradas neste release:** <!-- /health, /admin/... -->

## 🔌 Dependências do backend

- [ ] Nenhuma dependência nova de API
- [ ] Endpoints/mensagens usados **já estão** no backend do ambiente de destino: <!-- versão do backend no ambiente -->

## ⚙️ Configuração do ambiente de destino

- [ ] Sem variáveis novas
- [ ] Variáveis de runtime novas/alteradas já configuradas no ambiente: <!-- API_URL, WS_URL… -->
- [ ] `APP_CORS_ORIGINS` do backend do ambiente inclui o domínio do front

## ✅ Validação

**Antes do merge**

- [ ] Validação completa da branch de origem verde (lint, tipos, testes e E2E)
- [ ] Ambiente de origem saudável (`/healthz`, `/health`, `/admin/health`)
- [ ] (→ master) Homologação em **staging** concluída — responsável / evidência: <!-- link -->

**Depois do merge**

- [ ] Nova versão rodando no ambiente de destino
- [ ] `/healthz` = 200; `/health` e `/admin/health` mostram API `ok` (HTTP e WebSocket)
- [ ] Sem erros no console nas telas principais
- [ ] (→ master) Tag `frontend-vX.Y.Z` criada no commit de merge
- [ ] (back-merge) Correção do hotfix presente na branch de destino

## ↩️ Rollback

- Versão atual no ambiente de destino: `frontend-v`
- Rollback para: `frontend-v`

## 🔗 MRs relacionados

<!-- Release do backend no mesmo ambiente, hotfix que originou o back-merge… -->

## ✅ Checklist do release

- [ ] Título no formato `chore: promove …` / `chore: back-merge …`
- [ ] **"Delete source branch" desmarcado**
- [ ] Origem → destino permitidos pela matriz (CONTRIBUTING §1.3)
- [ ] Aprovações: ≥ 1 Maintainer (→ master: 2)

/assign me
