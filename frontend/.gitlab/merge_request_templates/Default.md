<!--
  FRONTEND — template padrão (feat, refactor, perf, test, build, chore).
  Título do MR = mensagem no padrão de commit, ex.: feat: [CPBS-123] adiciona tela de status
  Destino: developer · branch criada a partir da developer · merge commit (sem squash).
  Escopos: web · admin · frontend (shared, features comuns, config, Docker)
  Guia: CONTRIBUTING.md · Docs: docs/README.md
  Preencha todas as seções. O que não se aplicar: "N/A" + motivo.
-->

## 🎫 Ticket

CPBS-

## 🎯 Contexto

<!-- Qual problema este MR resolve e por quê. Link para ADR/discussão/design, se houver. -->

## 🛠️ O que mudou

-

## 🧩 Partes do frontend afetadas

- [ ] Área **web** (`src/app/(web)`, `src/areas/web`)
- [ ] Área **admin** (`src/app/admin`, `src/areas/admin`)
- [ ] Feature comum (`src/features/`) — qual:
- [ ] `src/shared/` (ui, api, ws, config, providers)
- [ ] Docker / compose / configs (`next.config.ts`, eslint, tsconfig)
- [ ] Documentação (`docs/`)

## 🖥️ Telas

| Rota | Nova / alterada | Descrição |
|------|-----------------|-----------|
| <!-- /admin/health --> | | |

## 🔌 Integração com a API

- [ ] Não consome endpoint/mensagem novos
- [ ] Consome contrato novo/alterado — `pnpm openapi` rodado contra a API em: <!-- local / dev --> e `openapi.json` + `schema.d.ts` commitados
- [ ] Depende de MR do backend: <!-- link — já está em produção? -->

## ⚙️ Configuração

- [ ] Sem novas variáveis de ambiente
- [ ] Novas variáveis (runtime) documentadas em `.env.example` e `docs/10-docker.md`: <!-- quais -->

## 🧪 Como testar

1. Subir a API e o banco no repositório do backend (`docker compose -f docker-compose.dev.yml up --build`)
2. Aqui: `docker compose -f docker-compose.dev.yml up --build`
3. Acessar <!-- http://localhost:3000/... -->

**Testes adicionados/alterados:**

- <!-- src/features/.../__tests__/... · src/app/.../page.test.tsx · e2e/... -->

## 📸 Evidências

<!-- Prints/GIF das telas (desktop e mobile quando fizer sentido). -->

## ⚠️ Riscos e pontos de atenção

<!-- Mudanças de layout compartilhado, dependências novas, impacto na outra área. -->

## 🔗 MRs relacionados

<!-- MR do backend relacionado, se houver. -->

## ✅ Checklist do autor

- [ ] Destino `developer`; commits organizados — todos no padrão, sem `wip` (sem squash, todos vão para o histórico)
- [ ] Branch e commits no padrão (`tipo/CPBS-xxx-descricao`, `tipo: [CPBS-xxx] ...`)
- [ ] Título do MR no formato `tipo: [CPBS-xxx] descrição`
- [ ] Testes escritos **antes/junto** (TDD): toda feature, hook e tela nova/alterada tem teste; tela nova tem E2E
- [ ] `make lint typecheck test` verde (eslint + fronteiras, prettier, tsc, vitest ≥ 80%)
- [ ] Fronteiras respeitadas: web ↛ admin, admin ↛ web, feature ↛ feature, import de feature só pelo `index.ts`
- [ ] Modo SPA respeitado: sem fetch de negócio em Server Components, sem Server Actions
- [ ] Sem `NEXT_PUBLIC_*` nem URL da API fixa no código (config de runtime)
- [ ] Acessibilidade básica (semântica, labels, foco visível)
- [ ] Tabelas de telas/features em `docs/05-area-web.md` / `docs/06-area-admin.md` atualizadas
- [ ] Sem segredos, `console.log`, código comentado ou TODO sem ticket

/assign me
