---
description: "Cria um bounded context novo completo (domain, application, infrastructure, presentation), com análise, testes, composição e docs"
agent: backend-ddd
argument-hint: "nome do context e o que ele faz (ex.: partners — cadastro de parceiros e seus serviços)"
---

Crie o bounded context **${input:context:nome do context em snake_case, ex.: partners}**.

Responsabilidade: ${input:descricao:o que este context faz e quais casos de uso iniciais}

Siga o [agente backend-ddd](../agents/backend-ddd.agent.md) — fases **Análise → Plano → Construção → Validação** — e as instruções em `.github/instructions/`. Use `api/contexts/health/` como referência.

## Fase 1 — Roteiro específico (além do roteiro comum do agente)

**Limites do context**
- [ ] Nome do context: termo de negócio, em inglês, snake_case, plural quando for coleção (`partners`)? Qual o termo em pt-BR para o glossário?
- [ ] O que **é** responsabilidade deste context e o que **não é** (e em qual context fica)?
- [ ] Relação com contexts existentes: quem consome quem e por qual caso de uso/evento? (sem import entre contexts)

**Modelo de domínio**
- [ ] Quais entidades e qual é o agregado raiz? Qual o identificador (formato do id)?
- [ ] Quais invariantes nunca podem ser violadas (ex.: documento único, status permitidos e transições)?
- [ ] Quais value objects (status, documento, dinheiro, período)?
- [ ] Termos da linguagem ubíqua que precisam entrar no glossário?

**Casos de uso iniciais**
- [ ] Lista dos casos de uso (verbo + substantivo), cada um com escopo (`public`/`admin`), canal (HTTP/WS) e exemplo de entrada → saída.

**Persistência**
- [ ] Tabela de padrões de acesso (quem consulta, por qual chave, ordenação, filtros) — monte a proposta de `PK`/`SK`/`GSI1` (docs/12, seção 3) e peça validação.
- [ ] Algum item expira (TTL)? Volume esperado por item/partição?
- [ ] Enquanto `api/core/dynamodb` não existir: confirmar uso de repositório em memória em `infrastructure/`.

## Entregáveis

1. Estrutura com `__init__.py` em todas as pastas:

   ```text
   api/contexts/<context>/
   ├── domain/          entities.py, value_objects.py, ports.py, errors.py (se houver erro de negócio)
   ├── application/     <verbo>_<substantivo>.py — um arquivo por caso de uso
   ├── infrastructure/  adapters das ports (+ codecs.py se converter dados externos)
   └── presentation/    schemas.py, dependencies.py, http.py, ws_handlers.py (se houver WS)
   ```

   As quatro camadas são obrigatórias (o contrato de camadas do import-linter exige todas, mesmo que alguma comece só com `__init__.py`).

2. Casos de uso definidos na análise, cada um com teste unitário.
3. Repositório como port no domínio; adapter conforme a decisão de persistência.
4. Endpoints e/ou mensagens WS no escopo decidido, incluídos em `api/routes/`.
5. Composição em `api/container.py`.
6. Testes: `tests/unit/contexts/<context>/…`, `tests/integration/api/test_<context>.py`, `tests/integration/websocket/test_<context>_ws.py` (se houver WS); fakes novos em `tests/fakes.py`.
7. Docs: endpoints/mensagens em `docs/06-contratos-api.md`, context em `docs/01-arquitetura.md`, termos em `docs/glossario.md`, `openapi.json` regenerado; análise em `docs/tasks/` se houver ticket.
