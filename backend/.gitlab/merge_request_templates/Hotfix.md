<!--
  BACKEND — HOTFIX: correção urgente de problema em produção (branches hotfix/*).
  Título do MR = cabeçalho no padrão de commit, ex.: fix(backend): aumenta timeout de leitura do websocket
  Branch criada a partir da master · destino: master · merge commit (sem squash).
  Depois do merge: tag de patch + back-merge master → staging → developer (template Release).
  Mudança MÍNIMA. Melhorias e refatorações vão em outro ticket.
-->

## 🚨 Ticket / incidente

- Ticket: CPBS-
- Incidente / alerta: <!-- link -->
- Início do problema: <!-- data e hora -->

## 🔥 Impacto em produção

- **Severidade:** <!-- crítica / alta / média -->
- **Escopo da API afetado:** <!-- public / admin / ambos -->
- **Endpoints / mensagens WS afetados:**
- **Sintoma:** <!-- erros 5xx, latência, WS caindo… -->
- **Evidências:** <!-- logs com X-Request-ID, métricas -->

## 🔍 Causa raiz

<!-- Conhecida ou provável. Se ainda não é conhecida, diga e abra ticket de investigação. -->

## 🛠️ Correção aplicada

-

## 🧪 Teste de regressão

- Arquivo: `tests/...`
- Teste:
- [ ] Confirmei que o teste **falha** sem a correção

## ↩️ Plano de rollback

- Imagem atual em produção: `backend:`
- Rollback para: `backend:`
- Passos:

## 📈 Validação pós-deploy

- [ ] `GET /api/v1/public/health` e `GET /api/v1/admin/health` retornando `ok`
- [ ] WebSocket respondendo `health.pong`
- [ ] Erros/latência voltaram ao normal
- [ ]

## 📌 Follow-up

- CPBS- <!-- correção definitiva, testes extras, post-mortem -->

## ✅ Checklist do autor

- [ ] Branch a partir da `master` atualizada: `hotfix/CPBS-xxx-descricao` · MR com destino `master`
- [ ] Mudança mínima, sem refatorações
- [ ] Teste de regressão adicionado
- [ ] `make lint typecheck test` verde
- [ ] Contrato **não** quebrado (ou frontend avisado)
- [ ] Plano de rollback preenchido
- [ ] Revisor(a) acionado(a) diretamente
- [ ] Após o merge: tag `backend-vX.Y.Z+1` na `master` e deploy de production aprovado
- [ ] Back-merge aberto no mesmo dia: MR `master → staging` e depois `staging → developer` (template Release) — links:

/assign me
/label ~hotfix ~bug ~backend
