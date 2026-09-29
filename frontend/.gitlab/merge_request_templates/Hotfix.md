<!--
  FRONTEND — HOTFIX: correção urgente de problema em produção (branches hotfix/*).
  Título do MR = cabeçalho no padrão de commit, ex.: fix(web): corrige tela em branco na página de status
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
- **Área afetada:** <!-- web (clientes) / admin (operação) / ambas -->
- **Rotas afetadas:**
- **Sintoma:** <!-- tela em branco, erro de CORS, WS desconectando… -->
- **Evidências:** <!-- prints, erros do console, logs -->

## 🔍 Causa raiz

<!-- Conhecida ou provável. Problema no front, na config de runtime (API_URL/WS_URL) ou na API? -->

## 🛠️ Correção aplicada

-

## 🧪 Teste de regressão

- Arquivo:
- Teste:
- [ ] Confirmei que o teste **falha** sem a correção

## ↩️ Plano de rollback

- Imagem atual em produção: `frontend:`
- Rollback para: `frontend:`
- Passos:

## 📈 Validação pós-deploy

- [ ] `GET /healthz` do front retornando 200
- [ ] `/health` e `/admin/health` mostrando API `ok` (HTTP e WebSocket)
- [ ] Sem erros no console nas rotas afetadas
- [ ]

## 📌 Follow-up

- CPBS- <!-- correção definitiva, testes extras, post-mortem -->

## ✅ Checklist do autor

- [ ] Branch a partir da `master` atualizada: `hotfix/CPBS-xxx-descricao` · MR com destino `master`
- [ ] Mudança mínima, sem refatorações
- [ ] Teste de regressão adicionado
- [ ] `make lint typecheck test` verde
- [ ] Plano de rollback preenchido
- [ ] Revisor(a) acionado(a) diretamente
- [ ] Após o merge: tag `frontend-vX.Y.Z+1` na `master` e deploy de production aprovado
- [ ] Back-merge aberto no mesmo dia: MR `master → staging` e depois `staging → developer` (template Release) — links:

/assign me
/label ~hotfix ~bug ~frontend
