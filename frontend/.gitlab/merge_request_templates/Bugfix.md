<!--
  FRONTEND — correção de bug (branches fix/*).
  Título do MR = mensagem no padrão de commit, ex.: fix: [CPBS-123] corrige status do websocket após reconexão
  Destino: developer · branch criada a partir da developer · merge commit (sem squash).
  Urgente em produção? Use o template Hotfix.
-->

## 🎫 Ticket

CPBS-

## 🐛 Comportamento atual

<!-- O que o usuário vê. Prints, erros do console, requisições com falha (X-Request-ID). -->

## ✔️ Comportamento esperado

## 🔁 Como reproduzir

1.
2.

**Área / rota:** <!-- web /health · admin /admin/health -->
**Navegador / dispositivo:** <!-- Chrome 1xx desktop, Safari iOS… -->
**Ambiente / versão:** <!-- local / dev / staging / produção — versão frontend-vX.Y.Z -->

## 🔍 Causa raiz

<!-- Por que acontecia: componente, hook, cache do TanStack Query, cliente WS, config… -->

## 🛠️ Correção

-

## 🧪 Teste de regressão (obrigatório)

- Arquivo: `src/.../__tests__/...` ou `e2e/...`
- Teste:
- [ ] Confirmei que o teste **falha** sem a correção

## 📸 Antes / depois

<!-- Prints ou GIF. -->

## ⚠️ Riscos

<!-- A correção afeta a outra área ou features comuns? -->

## ✅ Checklist do autor

- [ ] Destino `developer` (bug em produção urgente? use Hotfix); commits organizados, sem `wip`
- [ ] Branch e commits no padrão (`fix/CPBS-xxx-descricao`, `fix: [CPBS-xxx] ...`)
- [ ] Teste de regressão adicionado e falhando sem a correção
- [ ] `make lint typecheck test` verde
- [ ] Documentação atualizada, se o comportamento documentado mudou
- [ ] Sem segredos, `console.log` ou código comentado

/assign me
