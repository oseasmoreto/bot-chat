# ADR-0008 — Convenção de nomes: camelCase no TS e na API, PEP 8 no Python

- **Status:** Proposto (aguardando confirmação do time)
- **Data:** 2026-09-29
- **Ticket:** CPBS-275

## Contexto
A orientação da task é usar **camelCase para métodos**. No TypeScript isso é o padrão. No Python, a PEP 8 define `snake_case` para funções/métodos, e todo o ecossistema (stdlib, FastAPI, Pydantic) e o linter (`ruff`, regra `N802`) seguem isso.

## Decisão
- **TypeScript:** camelCase em funções, métodos e variáveis.
- **Python:** PEP 8 (`snake_case` em funções/métodos, `PascalCase` em classes).
- **Contrato externo** (JSON REST, payload WS, `operationId`): **camelCase**, convertido automaticamente por `BaseSchema` (`alias_generator=to_camel`).

Resultado: todo desenvolvedor de front e todo consumidor da API só enxerga camelCase; o Python continua idiomático.

## Alternativas consideradas
- **camelCase também no Python:** exigiria desligar regras do linter, conflitaria com nomes do FastAPI/Pydantic/stdlib e tornaria o código inconsistente dentro do mesmo arquivo.

## Consequências
- Tabelas de nomenclatura completas em [backend/08-padroes-python.md](../backend/08-padroes-python.md), [frontend-comum/05-padroes-typescript.md](../frontend-comum/05-padroes-typescript.md) e [06-padroes-gerais.md](../06-padroes-gerais.md).
- Se o time decidir camelCase também no Python, este ADR é substituído e o ruff precisa ignorar `N802`/`N803`/`N806`.
