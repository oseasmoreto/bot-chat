<!--
  Template de HOTFIX — correção urgente de problema em produção (branches hotfix/*).
  Título do MR = cabeçalho no padrão de commit, ex.: fix(infra): aumenta timeout do proxy websocket
  Mantenha a mudança MÍNIMA. Melhorias e refatorações vão em outro ticket.
  Guia completo: docs/08-branches-commits-mr.md
-->

## 🚨 Ticket / incidente

- Ticket: CPBS-
- Incidente / alerta: <!-- link -->
- Início do problema: <!-- data e hora -->

## 🔥 Impacto em produção

- **Severidade:** <!-- crítica / alta / média -->
- **Escopo afetado:** <!-- public (clientes) / admin (operação) / ambos -->
- **Sintoma:** <!-- o que usuários estão vendo -->
- **Usuários/parceiros impactados:** <!-- estimativa -->

## 🔍 Causa raiz

<!-- Conhecida ou provável. Se ainda não é conhecida, diga e abra ticket de investigação. -->

## 🛠️ Correção aplicada

<!-- A mudança MÍNIMA para restaurar o serviço. -->

-

## 🧩 Partes afetadas

- [ ] `backend/`
- [ ] `web/` (escopo public)
- [ ] `admin/` (escopo admin)
- [ ] `packages/`
- [ ] `infra/` (Nginx, Docker, supervisord, compose)

## 🧪 Teste de regressão

- Arquivo:
- Teste:
- [ ] Confirmei que o teste **falha** sem a correção

## ↩️ Plano de rollback

<!-- Como voltar se der errado: versão/tag anterior da imagem, passos, quem executa. -->

- Versão atual em produção: `v`
- Rollback para: `v`
- Passos:

## 📈 Validação pós-deploy

<!-- Como confirmar em produção que resolveu: health, métricas, logs, fluxo manual. -->

- [ ] `GET /api/v1/public/health` e `/api/v1/admin/health` retornando `ok`
- [ ]

## 📌 Follow-up

<!-- Tickets abertos para correção definitiva, testes extras, post-mortem. -->

- CPBS-

## ✅ Checklist do autor

- [ ] Branch a partir da `main` atualizada: `hotfix/CPBS-xxx-descricao`
- [ ] Mudança mínima, sem refatorações
- [ ] Teste de regressão adicionado
- [ ] `make lint typecheck test` verde
- [ ] Plano de rollback preenchido
- [ ] Revisor(a) acionado(a) diretamente (revisão prioritária)
- [ ] Após o merge: tag de patch (`vX.Y.Z+1`) e acompanhamento do deploy

/assign me
/label ~hotfix ~bug
