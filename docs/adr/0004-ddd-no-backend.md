# ADR-0004 — DDD com bounded contexts e camadas no backend

- **Status:** Aceito
- **Data:** 2026-09-29
- **Ticket:** CPBS-275

## Contexto
O backend será a base para **fluxos** e **integrações** com parceiros — domínio que vai crescer. Precisamos de isolamento entre áreas e testabilidade.

## Decisão
- Código organizado em `contexts/<nome>/` (bounded contexts).
- Cada context com `domain`, `application`, `infrastructure`, `presentation`.
- Domínio em Python puro; ports como `typing.Protocol`; adapters injetados no composition root (`container.py`).
- Fronteiras verificadas por `import-linter` no CI.
- `core/` como *shared kernel* mínimo.

## Alternativas consideradas
- **Estrutura por camada técnica global** (`routers/`, `services/`, `models/`): simples no início, mas mistura domínios quando cresce.
- **Framework de DI** (dependency-injector etc.): desnecessário agora; um dataclass `Container` basta (KISS).

## Consequências
- Mais arquivos para um endpoint simples (aceito em troca de consistência).
- Casos de uso testáveis sem FastAPI.
- Checklist de novo context documentado em [backend/README.md](../backend/README.md#checklist-para-criar-um-novo-context).
