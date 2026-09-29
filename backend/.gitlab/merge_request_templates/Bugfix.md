<!--
  BACKEND — correção de bug (branches fix/*).
  Título do MR = cabeçalho no padrão de commit, ex.: fix(backend): corrige status 503 do health quando componente degradado
  Destino: developer · branch criada a partir da developer · merge commit (sem squash).
  Urgente em produção? Use o template Hotfix.
-->

## 🎫 Ticket

CPBS-

## 🐛 Comportamento atual

<!-- O que acontece hoje: request, resposta, logs (com X-Request-ID), stack trace. -->

## ✔️ Comportamento esperado

## 🔁 Como reproduzir

1.
2.

**Ambiente / versão:** <!-- local / dev / staging / produção — APP_VERSION -->
**Endpoint / mensagem:** <!-- ex.: GET /api/v1/admin/health · health.ping em /api/v1/ws/public -->

## 🔍 Causa raiz

<!-- Por que acontecia. Em qual camada (domínio, caso de uso, adapter, rota, WS)? -->

## 🛠️ Correção

-

## 🧪 Teste de regressão (obrigatório)

- Arquivo: `tests/...`
- Teste:
- [ ] Confirmei que o teste **falha** sem a correção

## 🔌 Contrato

- [ ] Não mudou
- [ ] Mudou — `openapi.json` atualizado; impacto no frontend descrito: <!-- … -->

## ⚠️ Riscos

<!-- A correção pode afetar outros endpoints/escopos? -->

## ✅ Checklist do autor

- [ ] Destino `developer` (bug em produção urgente? use Hotfix); commits organizados, sem `wip`
- [ ] Branch e commits no padrão (`fix/CPBS-xxx-descricao`, `fix(backend): ...` com `Refs: CPBS-xxx`)
- [ ] Teste de regressão adicionado e falhando sem a correção
- [ ] `make lint typecheck test` verde
- [ ] Documentação atualizada, se o comportamento documentado mudou
- [ ] Sem segredos, `print` de debug ou código comentado

/assign me
/label ~bug ~backend
