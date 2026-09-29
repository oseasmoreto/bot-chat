<!--
  Template de correção de bug (branches fix/*).
  Título do MR = cabeçalho no padrão de commit, ex.: fix(ws-client): reconecta após queda de rede
  Urgente em produção? Use o template Hotfix.
  Guia completo: docs/08-branches-commits-mr.md
-->

## 🎫 Ticket

CPBS-

## 🐛 Comportamento atual (bug)

<!-- O que acontece hoje. Mensagens de erro, logs, prints. -->

## ✔️ Comportamento esperado

<!-- O que deveria acontecer. -->

## 🔁 Como reproduzir

1.
2.
3.

**Ambiente:** <!-- local / dev / staging / produção — versão (APP_VERSION) -->

## 🔍 Causa raiz

<!-- Por que o bug acontecia. Não apenas o sintoma. -->

## 🛠️ Correção

<!-- O que foi alterado para corrigir e por que esta abordagem. -->

-

## 🧩 Partes afetadas

- [ ] `backend/`
- [ ] `web/` (escopo public)
- [ ] `admin/` (escopo admin)
- [ ] `packages/` (ui, api-client, ws-client, config)
- [ ] `infra/` (Nginx, Docker, supervisord, compose)
- [ ] `docs/`

## 🧪 Teste de regressão

<!-- OBRIGATÓRIO: teste que falhava antes da correção e passa agora. Informe o arquivo e o nome do teste. -->

- Arquivo:
- Teste:
- [ ] Confirmei que o teste **falha** sem a correção

## 🧪 Como validar

1.
2.

## ⚠️ Riscos

<!-- A correção pode afetar outros fluxos? Qual? -->

## ✅ Checklist do autor

- [ ] Branch e commits no padrão (`fix/CPBS-xxx-descricao`, `fix(escopo): ...` com `Refs: CPBS-xxx`)
- [ ] Teste de regressão adicionado e falhando sem a correção
- [ ] `make lint typecheck test` verde localmente
- [ ] Contrato de API alterado? `make openapi` + docs atualizados (ou N/A)
- [ ] Documentação atualizada, se o comportamento documentado mudou
- [ ] Sem segredos, logs de debug ou código comentado

/assign me
/label ~bug
