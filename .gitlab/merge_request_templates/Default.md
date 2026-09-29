<!--
  Template padrão (feature, refactor, perf, test, build, ci, chore).
  Título do MR = cabeçalho no padrão de commit, ex.: feat(backend): adiciona health check por escopo
  Guia completo: docs/08-branches-commits-mr.md
  Preencha todas as seções. O que não se aplicar: escreva "N/A" e o motivo.
-->

## 🎫 Ticket

CPBS-

## 🎯 Contexto

<!-- Qual problema este MR resolve e por quê. Link para ADR/discussão, se houver. -->

## 🛠️ O que mudou

<!-- Lista objetiva das mudanças. Foque no "o quê" e nas decisões; o diff mostra o "como". -->

-

## 🧩 Partes afetadas

- [ ] `backend/`
- [ ] `web/` (escopo public)
- [ ] `admin/` (escopo admin)
- [ ] `packages/` (ui, api-client, ws-client, config)
- [ ] `infra/` (Nginx, Docker, supervisord, compose)
- [ ] `docs/`

## 🔌 Contrato de API / WebSocket

- [ ] Não mudou
- [ ] Mudou de forma compatível — `make openapi` rodado, `openapi.json` e `schema.d.ts` commitados, `docs/backend/05-contratos-api.md` atualizado
- [ ] **Breaking change** — descrito abaixo, commit com `!` e rodapé `BREAKING CHANGE:`, label ~"breaking-change"

<!-- Se breaking: o que quebra e como os consumidores devem migrar. -->

## 🧪 Como testar

<!-- Passo a passo para o revisor validar localmente. -->

1. `make up` (ou `make dev`)
2.
3.

**Testes adicionados/alterados:**

<!-- Liste os arquivos de teste. Toda rota, feature e tela nova/alterada precisa de teste. -->

-

## 📸 Evidências

<!-- Prints/GIF das telas (web/admin), saída de curl, logs relevantes. N/A se não houver UI. -->

## ⚠️ Riscos e pontos de atenção

<!-- Impactos possíveis, migrações, configurações novas (.env), dependências adicionadas. -->

## ✅ Checklist do autor

- [ ] Branch e commits no padrão (`tipo/CPBS-xxx-descricao`, Conventional Commits com `Refs: CPBS-xxx`)
- [ ] Título do MR no formato `tipo(escopo): descrição`
- [ ] Testes escritos **antes/junto** da implementação (TDD) para toda rota/feature/tela nova ou alterada
- [ ] `make lint typecheck test` verde localmente
- [ ] Fronteiras respeitadas (camadas DDD no backend; features isoladas; `web` ↔ `admin` sem imports cruzados)
- [ ] Documentação em `docs/` atualizada (estrutura, contratos, telas, ADR se houve decisão)
- [ ] Novas variáveis de ambiente documentadas em `.env.example` e `docs/04-docker-deploy.md`
- [ ] Sem segredos, `console.log`/`print` de debug, código comentado ou TODO sem ticket
- [ ] MR com tamanho revisável (~400 linhas, sem contar arquivos gerados)

/assign me
/label ~feature
