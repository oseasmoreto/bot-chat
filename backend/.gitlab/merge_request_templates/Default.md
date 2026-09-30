<!--
  BACKEND — template padrão (feat, refactor, perf, test, build, chore).
  Título do MR = cabeçalho no padrão de commit, ex.: feat(backend): adiciona health check por escopo
  Destino: developer · branch criada a partir da developer · merge commit (sem squash).
  Guia: CONTRIBUTING.md · Docs: docs/README.md
  Preencha todas as seções. O que não se aplicar: "N/A" + motivo.
-->

## 🎫 Ticket

CPBS-

## 🎯 Contexto

<!-- Qual problema este MR resolve e por quê. Link para ADR/discussão, se houver. -->

## 🛠️ O que mudou

-

## 🧩 Partes do backend afetadas

- [ ] Domínio (`contexts/*/domain`) — entidades, value objects, ports
- [ ] Aplicação (`contexts/*/application`) — casos de uso
- [ ] Infraestrutura (`contexts/*/infrastructure`) — adapters
- [ ] Apresentação — rotas HTTP (`/api/v1/public`, `/api/v1/admin`)
- [ ] WebSocket — mensagens (`/api/v1/ws/public`, `/api/v1/ws/admin`)
- [ ] `core/` (config, erros, logging, CORS, dispatcher)
- [ ] Persistência (DynamoDB: tabelas, chaves, índices, repositórios)
- [ ] Docker / compose
- [ ] Documentação (`docs/`)

**Escopos da API afetados:** <!-- public / admin / ambos / nenhum -->

## 🔌 Contrato (REST / WebSocket)

- [ ] Não mudou
- [ ] Mudou de forma **retrocompatível** — `make openapi` rodado, `openapi.json` commitado, `docs/06-contratos-api.md` atualizado
- [ ] **Breaking change** — nova versão de rota (`/api/v2`) ou coordenação descrita abaixo; commit com `!` e `BREAKING CHANGE:`; label ~"breaking-change"

**Impacto no frontend:** <!-- nenhum / precisa de MR no front: link ou ticket -->

## ⚙️ Configuração

- [ ] Sem novas variáveis de ambiente
- [ ] Novas variáveis documentadas em `.env.example` e `docs/08-docker.md`: <!-- quais -->
- [ ] Mudou `APP_CORS_ORIGINS` / regras de CORS ou `Origin` do WS: <!-- o quê -->
- [ ] Tabela ou índice novo no DynamoDB: definição em `core/dynamodb/tables.py` + padrões de acesso documentados + IaC dos ambientes: <!-- quais -->

## 🧪 Como testar

1. `make dev`
2. <!-- ex.: curl http://localhost:8000/api/v1/public/health -->
3.

**Testes adicionados/alterados:**

- <!-- tests/unit/... · tests/integration/... -->

## ⚠️ Riscos e pontos de atenção

<!-- Performance, dependências novas, mudanças de comportamento. -->

## 🔗 MRs relacionados

<!-- MR do frontend que depende/consome esta mudança, se houver. -->

## ✅ Checklist do autor

- [ ] Destino `developer`; commits organizados — todos no padrão, sem `wip` (sem squash, todos vão para o histórico)
- [ ] Branch e commits no padrão (`tipo/CPBS-xxx-descricao`, `tipo(backend): ...` com `Refs: CPBS-xxx`)
- [ ] Título do MR no formato `tipo(backend): descrição`
- [ ] Testes escritos **antes/junto** (TDD): toda rota e mensagem WS nova/alterada tem teste de integração; casos de uso com teste unitário
- [ ] `make lint typecheck test` verde (ruff, mypy --strict, lint-imports, pytest ≥ 90%)
- [ ] Camadas DDD respeitadas (domínio sem FastAPI/Pydantic; presentation não acessa infrastructure direto)
- [ ] `openapi.json` atualizado se o contrato mudou (teste de contrato verde)
- [ ] Documentação em `docs/` atualizada; ADR se houve decisão
- [ ] Sem segredos, `print` de debug, código comentado ou TODO sem ticket

/assign me
/label ~feature ~backend
