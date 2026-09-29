# ADR-0005 — Convenção de nomes: PEP 8 no Python, camelCase no contrato

- **Status:** Aceito
- **Data:** 2026-09-29

## Contexto
A orientação do projeto é usar **camelCase para métodos**. No Python, a PEP 8 define `snake_case` para funções/métodos, e o ecossistema (stdlib, FastAPI, Pydantic) e o linter (`ruff`, regra `N802`) seguem isso.

## Decisão
- **Python:** PEP 8 (`snake_case` em funções/métodos, `PascalCase` em classes).
- **Contrato externo** (JSON REST, payload WS, `operationId`): **camelCase**, via `BaseSchema` (`alias_generator=to_camel`).

## Alternativas consideradas
- **camelCase também no Python:** exigiria desligar regras do linter e conflitaria com nomes do FastAPI/Pydantic/stdlib.

## Consequências
- O frontend só enxerga camelCase.
- O `ruff` mantém as regras de nomenclatura PEP 8 (`N8xx`) ativas.
