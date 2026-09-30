# 14 — IA: GitHub Copilot no VS Code

O projeto usa o **GitHub Copilot** (chat e modo agente) no VS Code. A pasta `.github/` ensina ao Copilot a arquitetura, os padrões e o fluxo de trabalho do backend, para que o código gerado já saia no padrão — e as mesmas regras continuam garantidas por ruff, mypy, import-linter e testes.

## 1. Arquivos

```text
.github/
├── copilot-instructions.md              # regras gerais — aplicadas a toda conversa
├── instructions/                        # regras por pasta, aplicadas conforme o arquivo em edição
│   ├── domain.instructions.md           # api/contexts/**/domain/**
│   ├── application.instructions.md      # api/contexts/**/application/**
│   ├── infrastructure.instructions.md   # api/contexts/**/infrastructure/**
│   ├── presentation.instructions.md     # api/contexts/**/presentation/**, api/routes/**
│   ├── core.instructions.md             # api/core/**, app_run.py, config.py, container.py
│   ├── tests.instructions.md            # tests/**
│   └── dependencies.instructions.md     # requirements*.txt, pyproject.toml
├── prompts/                             # comandos "/" no chat
│   ├── novo-context.prompt.md
│   ├── novo-modulo.prompt.md
│   ├── novo-endpoint.prompt.md
│   ├── nova-mensagem-ws.prompt.md
│   └── revisar-arquitetura.prompt.md
└── agents/
    └── backend-ddd.agent.md             # agente especialista do backend
```

| Tipo | Quando o Copilot usa | Para quê |
|------|----------------------|----------|
| `copilot-instructions.md` | Sempre, em toda conversa do projeto | Stack, estrutura, fronteiras DDD, convenções, testes, validação, commits |
| `*.instructions.md` | Automaticamente quando o arquivo em edição casa com o `applyTo` | Regras detalhadas de cada camada |
| `*.prompt.md` | Quando você digita `/<nome>` no chat | Roteiro completo de uma tarefa recorrente, com campos a preencher |
| `*.agent.md` | Quando você escolhe o agente no seletor do chat (ou um prompt o aciona) | Persona especialista com fluxo de trabalho fixo: perguntar → planejar → TDD → implementar → validar |

## 2. Como usar

1. Abra a **pasta do backend** como workspace no VS Code (o Copilot lê o `.github/` da raiz do workspace).
2. Confirme que o Copilot Chat está ativo e em **modo agente**.
3. Rode um dos prompts no chat:

| Comando | Faz |
|---------|-----|
| `/novo-context` | Bounded context completo: quatro camadas, casos de uso iniciais, composição no container, rotas/mensagens, testes, OpenAPI e docs |
| `/novo-modulo` | Funcionalidade nova em um context existente: caso de uso + ports/adapters + exposição HTTP/WS |
| `/novo-endpoint` | Endpoint REST com schemas, testes, `operation_id`, OpenAPI e `docs/06` |
| `/nova-mensagem-ws` | Tipo de mensagem WebSocket: handler, registro no dispatcher, testes e `docs/06` |
| `/revisar-arquitetura` | Revisão das mudanças pendentes contra camadas, contrato, erros, testes, dependências e docs (só relatório) |

Todos os prompts rodam com o agente **`backend-ddd`**, que trabalha em quatro fases, sem pular nenhuma:

1. **Análise** — roteiro fixo de perguntas ([§3](#3-análise-antes-de-construir)); nenhum código antes da confirmação.
2. **Plano** — arquivos por camada, contrato (paths, `operationId`, schemas, mensagens, erros) e testes; aguarda o "ok".
3. **Construção** — testes primeiro, depois domain → application → infrastructure → presentation → composição; atualiza `openapi.json` e docs.
4. **Validação e resumo** — ruff, mypy, lint-imports, pytest com cobertura; só conclui com tudo verde. Nunca faz commit, push ou tag.

Também é possível conversar direto com o agente: selecione **backend-ddd** no seletor de agentes do chat e descreva a tarefa.

### Exemplo

```text
/novo-context
  context: partners
  descricao: cadastro de parceiros de varejo. Casos de uso: criar parceiro (admin),
             buscar por id (admin), listar ativos (public). Campos: nome, documento, status.
```

## 3. Análise antes de construir

Para a análise ser **consistente** — as mesmas perguntas, na mesma ordem, qualquer que seja o desenvolvedor ou a conversa — todo agente/prompt que constrói algo usa um roteiro fixo:

| Roteiro | Onde está | Cobre |
|---------|-----------|-------|
| **Comum** | `agents/backend-ddd.agent.md` | Negócio (problema, exemplos, regras, fora de escopo), contrato e acesso (escopo, canal, quem executa, compatibilidade com o front), erros e `code`s, dados (campos, LGPD, persistência, padrões de acesso, concorrência), integrações e configuração, não funcionais (paginação, idempotência, logs) |
| `/novo-context` | `prompts/novo-context.prompt.md` | Limites do context, relação com outros contexts, agregado raiz e invariantes, value objects, linguagem ubíqua, casos de uso iniciais, tabela de padrões de acesso (`PK`/`SK`/`GSI`) |
| `/novo-modulo` | `prompts/novo-modulo.prompt.md` | Se a funcionalidade pertence ao context, reaproveitamento, mudança em entidades já persistidas, invariantes, efeitos colaterais, idempotência e concorrência, exposição |
| `/novo-endpoint` | `prompts/novo-endpoint.prompt.md` | Método e path, `operationId`, parâmetros, paginação/filtros, status de sucesso, resposta, erros por status, idempotência, impacto no front |
| `/nova-mensagem-ws` | `prompts/nova-mensagem-ws.prompt.md` | Requisição→resposta ou push, `type`s, escopos, payloads, erros, frequência, equivalência com HTTP |

Como a análise acontece:

1. O agente lê o código e os docs e marca como **Já definido** (com a fonte) o que já está respondido.
2. Faz **todas as perguntas restantes de uma vez**, numeradas e agrupadas, cada uma com uma **sugestão** — dá para responder só "ok" ou "2: …".
3. Detalhe que não bloqueia vira **Assumido** (com a sugestão); o que bloqueia contrato ou modelo é perguntado de novo.
4. Fecha com a **tabela de decisões** e pede confirmação antes do plano.
5. Com ticket (`CPBS-<n>`), a análise é registrada em `docs/tasks/CPBS-<n>-<slug>.md`.

Tarefas pequenas sem decisão de contrato ou modelo (typo, renomear variável local) dispensam a análise.

## 4. Validação das regras

As instruções orientam o Copilot; quem **garante** as regras é a pipeline. O que o Copilot gerar passa pelas mesmas verificações de qualquer código:

| Regra | Verificada por |
|-------|----------------|
| Fronteiras entre camadas e entre contexts | `lint-imports` — contratos em `pyproject.toml` com `api.contexts.*` ([03](./03-arquitetura-ddd.md)) |
| Tipagem | `mypy --strict` |
| Estilo e nomes | `ruff check` / `ruff format` |
| Comportamento e cobertura ≥ 90% | `coverage run -m pytest` |
| Contrato | teste de contrato (`openapi.json` versionado = gerado) |

Código gerado por IA é revisado no MR como qualquer outro ([CONTRIBUTING.md](../CONTRIBUTING.md)).

## 5. Manutenção

- Mudou uma regra do projeto (doc, ADR, padrão)? Atualize no mesmo MR a instrução correspondente em `.github/` — as instruções não podem contradizer os docs.
- Tarefa repetitiva nova → novo `*.prompt.md` com frontmatter `description`, `agent: backend-ddd` e campos `${input:nome:dica}`.
- **Todo agente ou prompt que constrói algo tem uma fase de Análise com roteiro de perguntas** (checklist) — o comum do agente + um específico da tarefa, no mesmo formato dos existentes. Prompt só de leitura/revisão (como `/revisar-arquitetura`) dispensa.
- Pergunta que se repete nas análises e sempre tem a mesma resposta vira regra nos docs/instruções e sai do roteiro.
- Regra específica de uma pasta → novo `*.instructions.md` com `applyTo` (glob relativo à raiz do projeto).
- Mantenha as instruções curtas e objetivas; detalhes ficam nos docs, referenciados por link.
